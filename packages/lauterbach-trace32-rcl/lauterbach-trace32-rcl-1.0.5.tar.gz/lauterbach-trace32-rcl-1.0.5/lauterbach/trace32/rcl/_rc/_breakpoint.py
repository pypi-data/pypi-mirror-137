import enum

from ._address import Address
from .common import int2bytearray
from typing import List


class Breakpoint:
    def __init__(self, conn, *, action=None, address=None, type_=None, impl=None, enabled=True):
        self.__conn = conn
        self.action = action
        self.address = address
        self.enabled = enabled
        self.impl = impl
        self.type_ = type_

    def __str__(self):
        return "{{address: {}, type_: {}, impl: {}, action: {}, enabled: {}}}".format(
            str(self.__address),
            "None" if self.__type is None else self.__type.name,
            "None" if self.__impl is None else self.__impl.name,
            "None" if self.__action is None else self.__action.name,
            "True" if self.__enabled else "False",
        )

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        if action is None:
            self.__action = None
        elif isinstance(action, self.Action):
            self.__action = action
        elif isinstance(action, str):
            self.__action = self.Action[action]
        else:
            raise TypeError("breakpoint action has invalid type {}".format(type(action)))

    @property
    def address(self):
        """The breakpoint's address.

        :getter: Returns this symbols name.
        :setter: Sets this symbol's name.
        :type: string
        """
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        self.__enabled = enabled

    @property
    def impl(self):
        return self.__impl

    @impl.setter
    def impl(self, impl):
        if impl is None:
            self.__impl = None
        elif isinstance(impl, self.Impl):
            self.__impl = impl
        elif isinstance(impl, str):
            self.__impl = self.Impl[impl]
        else:
            raise TypeError("breakpoint impl has invalid type {}".format(type(impl)))

    @property
    def type_(self):
        return self.__type

    @type_.setter
    def type_(self, type_):
        if type_ is None:
            self.__type = None
        elif isinstance(type_, self.Type):
            self.__type = type_
        elif isinstance(type_, str):
            self.__type = self.Type[type_]
        else:
            raise TypeError("breakpoint type_ has invalid type {}".format(type(type_)))

    class Action(enum.IntEnum):
        NONE = 0x00
        STOP = 0x01
        SPOT = 0x02
        ALPHA = 0x04
        BETA = 0x08
        CHARLIE = 0x10
        DELTA = 0x20
        ECHO = 0x40

    class Type(enum.IntEnum):
        DELETED = 0x00
        PROGRAM = 0x01
        READ = 0x02
        WRITE = 0x04
        RW = 0x06

    class Impl(enum.IntEnum):
        AUTO = 0x00
        SOFT = 0x01
        ONCHIP = 0x02
        HARD = 0x04
        MARK = 0x08

    def delete(self):
        """Delete Breakpoint."""
        return self.__conn.library.t32_deletebreakpointobj(self)

    def disable(self):
        """Disable breakpoint."""
        # workaround, delete bp first, then set disabled bp.
        # otherwise we end up with two breakpoints when attempting to overwrite the old one
        self.delete()
        self.enabled = False
        recv_buffer = self.__conn.library.t32_writebreakpointobj(self)
        return self.deserialize(recv_buffer)

    def enable(self):
        """Enable breakpoint."""
        self.delete()
        self.enabled = True
        recv_buffer = self.__conn.library.t32_writebreakpointobj(self)
        return self.deserialize(recv_buffer)

    def set(self):
        """Set Breakpoint."""
        recv_buffer = self.__conn.library.t32_writebreakpointobj(self)
        return self.deserialize(recv_buffer)

    def deserialize(self, recv_buffer):

        read_ptr = 0
        parameter_id_len = 2

        while read_ptr < len(recv_buffer):

            parameter_id = bytes(recv_buffer[read_ptr : read_ptr + parameter_id_len])

            if parameter_id == b"SZ":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 8
                # self.size = int.from_bytes(recv_buffer[read_ptr:next_read_ptr], byteorder="little")

            elif parameter_id == b"AD":
                read_ptr += parameter_id_len
                (addr_params_size, address) = Address.deserialize(self.__conn, recv_buffer[read_ptr:])
                next_read_ptr = read_ptr + addr_params_size
                self.address = address

            elif parameter_id == b"TY":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 4
                self.type_ = Breakpoint.Type(int.from_bytes(recv_buffer[read_ptr:next_read_ptr], byteorder="little"))

            elif parameter_id == b"DM" or parameter_id == b"IM":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 4
                self.impl = Breakpoint.Impl(int.from_bytes(recv_buffer[read_ptr:next_read_ptr], byteorder="little"))

            elif parameter_id == b"jj":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 0
                self.type_ = Breakpoint.Type(0)
                self.impl = Breakpoint.Impl(0)
                break

            elif parameter_id == b"hh":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 2
                # not really used here:
                # xxindex = int.from_bytes(recv_buffer[read_ptr:next_read_ptr])

            elif parameter_id == b"CA":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 4
                self.action = Breakpoint.Action(int.from_bytes(recv_buffer[read_ptr:next_read_ptr], byteorder="little"))

            elif parameter_id == b"EN":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 2
                self.enabled = (int.from_bytes(recv_buffer[read_ptr:next_read_ptr], byteorder="little")) == 1

            elif parameter_id == b"XX":
                read_ptr += parameter_id_len
                break

            else:
                raise ValueError()

            read_ptr = next_read_ptr

        return self

    def serialize(self):

        result = b"AD"
        addr_params_size, addr_params = self.address.serialize()
        result += addr_params

        # TODO Breakpoint needs Size parameter!
        #        if self.size is not None:
        #            result += b"SZ"
        #            result += int2bytearray(self.size, 8)
        #        else:
        result += b"SZ"
        result += int2bytearray(0x00, 8)

        if self.type_ is not None:
            result += b"TY"
            result += int2bytearray(self.type_.value, 4)
        else:
            result += b"TY"
            result += int2bytearray(Breakpoint.Type.PROGRAM, 4)

        if self.impl is not None:
            result += b"IM"
            result += int2bytearray(self.impl.value, 4)
        else:
            result += b"IM"
            result += int2bytearray(Breakpoint.Impl.AUTO, 4)

        if self.action is not None:
            result += b"CA"
            result += int2bytearray(self.action, 4)
        else:
            result += b"CA"
            result += int2bytearray(Breakpoint.Action.NONE, 4)

        result += b"EN"
        if self.enabled:
            result += int2bytearray(0x01, 2)
        else:
            result += int2bytearray(0x00, 2)

        result += b"XX"  # = end marker
        result += int2bytearray(0x00, 2)

        return len(result), result


breakpoint_list = List[Breakpoint]


class BreakpointService:
    def __init__(self, conn):
        self.__conn = conn

    def __call__(self, *args, **kwargs):
        return Breakpoint(self.__conn, *args, **kwargs)

    def _breakpoint_list(self) -> breakpoint_list:
        bp_count = self.__conn.library.t32_querybreakpointobjcount()
        bps = []
        for bp_i in range(bp_count):
            recv_buffer = self.__conn.library.t32_readbreakpointobjbyindex(bp_i)
            bps.append(Breakpoint(self.__conn).deserialize(recv_buffer))

        return bps

    def set(self, *args, **kwargs) -> Breakpoint:
        """Set breakpoint

        Returns:
            Breakpoint: Result
        """
        return Breakpoint(self.__conn, *args, **kwargs).set()

    def list(self) -> breakpoint_list:
        """
        Returns a list of the currently set Breakpoints

        Returns:
            List[Breakpoint]: Result
        """
        return self._breakpoint_list()
