## Good example with ABC event

[[tags]]: [[ready_sol]] [[python]] [[event]] [[DDD]]
[[uniq_link]]: "cbe58a31-9858-42f9-9f53-8358ebe9d357"
[[asked_question]]: "How to use ABC for event ?"

---

```
basic.py:
	T = TypeVar("T", bound=BaseModel)

	class BaseEvent(Generic[T], ABC):
	    @abstractmethod
	    async def handle(self, payload: T) -> None:
	        ...


event.py:
	class UserCreatedEvent(BaseEvent[UserCreateDTO]):
	    async def handle(self, payload: UserCreateDTO):
	        ...


```

#### If we need to particular data but we need to define event appart we need to pass generic inside the handle.
