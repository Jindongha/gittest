# postgresql/json.py
# Copyright (C) 2005-2014 the SQLAlchemy authors and contributors <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import absolute_import

import json

from .base import ischema_names
from ... import types as sqltypes
from ...sql.operators import custom_op
from ... import sql
from ...sql import elements
from ... import util

__all__ = ('JSON', 'JSONElement')


class JSONElement(elements.BinaryExpression):
    """Represents accessing an element of a :class:`.JSON` value.

    The :class:`.JSONElement` is produced whenever using the Python index
    operator on an expression that has the type :class:`.JSON`::

        expr = mytable.c.json_data['some_key']

    The expression typically compiles to a JSON access such as ``col -> key``.
    Modifiers are then available for typing behavior, including :meth:`.JSONElement.cast`
    and :attr:`.JSONElement.astext`.

    """
    def __init__(self, left, right, astext=False, opstring=None, result_type=None):
        self._astext = astext
        if opstring is None:
            if hasattr(right, '__iter__') and \
                not isinstance(right, util.string_types):
                opstring = "#>"
                right = "{%s}" % (", ".join(util.text_type(elem) for elem in right))
            else:
                opstring = "->"

        self._json_opstring = opstring
        operator = custom_op(opstring, precedence=5)
        right = left._check_literal(left, operator, right)
        super(JSONElement, self).__init__(left, right, operator, type_=result_type)

    @property
    def astext(self):
        """Convert this :class:`.JSONElement` to use the 'astext' operator
        when evaluated.

        E.g.::

            select([data_table.c.data['some key'].astext])

        .. seealso::

            :meth:`.JSONElement.cast`

        """
        if self._astext:
            return self
        else:
            return JSONElement(
                    self.left,
                    self.right,
                    astext=True,
                    opstring=self._json_opstring + ">",
                    result_type=sqltypes.String(convert_unicode=True)
                )

    def cast(self, type_):
        """Convert this :class:`.JSONElement` to apply both the 'astext' operator
        as well as an explicit type cast when evaulated.

        E.g.::

            select([data_table.c.data['some key'].cast(Integer)])

        .. seealso::

            :attr:`.JSONElement.astext`

        """
        if not self._astext:
            return self.astext.cast(type_)
        else:
            return sql.cast(self, type_)


class JSON(sqltypes.TypeEngine):
    """Represent the Postgresql JSON type.

    The :class:`.JSON` type stores arbitrary JSON format data, e.g.::

        data_table = Table('data_table', metadata,
            Column('id', Integer, primary_key=True),
            Column('data', JSON)
        )

        with engine.connect() as conn:
            conn.execute(
                data_table.insert(),
                data = {"key1": "value1", "key2": "value2"}
            )

    :class:`.JSON` provides several operations:

    * Index operations::

        data_table.c.data['some key']

    * Index operations returning text (required for text comparison)::

        data_table.c.data['some key'].astext == 'some value'

    * Index operations with a built-in CAST call::

        data_table.c.data['some key'].cast(Integer) == 5

    * Path index operations::

        data_table.c.data[('key_1', 'key_2', ..., 'key_n')]

    * Path index operations returning text (required for text comparison)::

        data_table.c.data[('key_1', 'key_2', ..., 'key_n')].astext == 'some value'

    Index operations return an instance of :class:`.JSONElement`, which represents
    an expression such as ``column -> index``.  This element then defines
    methods such as :attr:`.JSONElement.astext` and :meth:`.JSONElement.cast`
    for setting up type behavior.

    The :class:`.JSON` type, when used with the SQLAlchemy ORM, does not detect
    in-place mutations to the structure.  In order to detect these, the
    :mod:`sqlalchemy.ext.mutable` extension must be used.  This extension will
    allow "in-place" changes to the datastructure to produce events which
    will be detected by the unit of work.  See the example at :class:`.HSTORE`
    for a simple example involving a dictionary.

    Custom serializers and deserializers are specified at the dialect level,
    that is using :func:`.create_engine`.  The reason for this is that when
    using psycopg2, the DBAPI only allows serializers at the per-cursor
    or per-connection level.   E.g.::

        engine = create_engine("postgresql://scott:tiger@localhost/test",
                                json_serializer=my_serialize_fn,
                                json_deserializer=my_deserialize_fn
                        )

    When using the psycopg2 dialect, the json_deserializer is registered
    against the database using ``psycopg2.extras.register_default_json``.

    .. versionadded:: 0.9

    """

    __visit_name__ = 'JSON'

    class comparator_factory(sqltypes.Concatenable.Comparator):
        """Define comparison operations for :class:`.JSON`."""

        def __getitem__(self, other):
            """Get the value at a given key."""

            return JSONElement(self.expr, other)

        def _adapt_expression(self, op, other_comparator):
            if isinstance(op, custom_op):
                if op.opstring == '->':
                    return op, sqltypes.Text
            return sqltypes.Concatenable.Comparator.\
                _adapt_expression(self, op, other_comparator)

    def bind_processor(self, dialect):
        json_serializer = dialect._json_serializer or json.dumps
        if util.py2k:
            encoding = dialect.encoding
            def process(value):
                return json_serializer(value).encode(encoding)
        else:
            def process(value):
                return json_serializer(value)
        return process

    def result_processor(self, dialect, coltype):
        json_deserializer = dialect._json_deserializer or json.loads
        if util.py2k:
            encoding = dialect.encoding
            def process(value):
                return json_deserializer(value.decode(encoding))
        else:
            def process(value):
                return json_deserializer(value)
        return process


ischema_names['json'] = JSON
