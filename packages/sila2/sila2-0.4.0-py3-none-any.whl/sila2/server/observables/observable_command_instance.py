from __future__ import annotations

from datetime import timedelta
from queue import Queue
from typing import Generic, Optional, TypeVar

from sila2.framework import CommandExecutionInfo, CommandExecutionStatus


class ObservableCommandInstance:
    __progress: Optional[float]
    __estimated_remaining_time: Optional[timedelta]
    __status: Optional[CommandExecutionStatus]
    __info_queue: Queue[CommandExecutionInfo]

    def __init__(self, execution_info_queue: Queue[CommandExecutionInfo]):
        self.__progress = 0
        self.__estimated_remaining_time = None
        self.__status = None
        self.__info_queue = execution_info_queue

    @property
    def status(self) -> Optional[CommandExecutionStatus]:
        return self.__status

    @status.setter
    def status(self, status: CommandExecutionStatus) -> None:
        if not isinstance(status, CommandExecutionStatus):
            raise TypeError(f"Expected a {CommandExecutionStatus.__class__.__name__}, got {status}")
        self.__status = status
        self.__update_execution_info()

    @property
    def progress(self) -> float:
        return self.__progress

    @progress.setter
    def progress(self, progress: float) -> None:
        if not isinstance(progress, (int, float)):
            raise TypeError(f"Expected an int or float, got {progress}")
        if progress < 0 or progress > 100:
            raise ValueError("Progress must be between 0 and 100")
        self.__progress = progress
        self.__update_execution_info()

    @property
    def estimated_remaining_time(self) -> Optional[timedelta]:
        return self.__estimated_remaining_time

    @estimated_remaining_time.setter
    def estimated_remaining_time(self, estimated_remaining_time: timedelta) -> None:
        if not isinstance(estimated_remaining_time, timedelta):
            raise TypeError(f"Expected a datetime.timedelta, got {estimated_remaining_time}")
        if estimated_remaining_time.total_seconds() < 0:
            raise ValueError("Estimated remaining time cannot be negative")
        self.__estimated_remaining_time = estimated_remaining_time
        self.__update_execution_info()

    def __update_execution_info(self) -> None:
        if self.__status is None:
            self.__status = CommandExecutionStatus.running

        self.__info_queue.put(CommandExecutionInfo(self.__status, self.__progress, self.__estimated_remaining_time))


IntermediateResponseType = TypeVar("IntermediateResponseType")


class ObservableCommandInstanceWithIntermediateResponses(ObservableCommandInstance, Generic[IntermediateResponseType]):
    __intermediate_response_queue: Queue[IntermediateResponseType]

    def __init__(
        self,
        execution_info_queue: Queue[CommandExecutionInfo],
        intermediate_response_queue: Queue[IntermediateResponseType],
    ):
        super().__init__(execution_info_queue)
        self.__intermediate_response_queue = intermediate_response_queue

    def send_intermediate_response(self, value: IntermediateResponseType) -> None:
        self.__intermediate_response_queue.put(value)
