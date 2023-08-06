from abc import ABC, abstractmethod
from typing import Type

from datek_async_fsm.state import BaseState as _BaseState, StateCollection, StateType

from datek_jaipur.application.state_machine.scope import Scope
from datek_jaipur.errors import JaipurError


class BaseState(_BaseState, ABC):
    async def transit(self, states: StateCollection) -> Type["BaseState"]:
        while True:
            try:
                return await self.get_next_state(states)
            except JaipurError:
                pass

    @abstractmethod
    async def get_next_state(self, states: StateCollection) -> Type["BaseState"]:
        pass


class Start(BaseState):
    scope: Scope

    @staticmethod
    def type() -> StateType:
        return StateType.INITIAL

    async def get_next_state(self, states: StateCollection) -> Type["BaseState"]:
        adapter = self.scope.adapter_class(self.__class__)
        self.scope.game = await adapter.collect_data()
        return PlayerTurn


class PlayerTurn(BaseState):
    scope: Scope

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    async def get_next_state(self, states: StateCollection) -> Type["BaseState"]:
        adapter = self.scope.adapter_class(
            state_class=self.__class__,
            game=self.scope.game,
        )

        self.scope.game = await adapter.collect_data()

        return PlayerWon if self.scope.game.winner else PlayerTurn


class PlayerWon(BaseState):
    scope: Scope

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    async def get_next_state(self, states: StateCollection) -> Type["BaseState"]:
        adapter = self.scope.adapter_class(
            state_class=self.__class__,
            game=self.scope.game,
        )

        return await adapter.collect_data()


class End(BaseState, ABC):
    @staticmethod
    def type() -> StateType:
        return StateType.END
