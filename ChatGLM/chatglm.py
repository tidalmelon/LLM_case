from langchain.llms.base import BaseLLM
from typing import (
    Any,
    Dict,
    Literal,
    Union,
    AbstractSet,
    Collection,
)
from langchain_core.pydantic_v1 import Field, root_validator






class ChatGLM(BaseLLM):
    """zhipuai large language model class."""

    
    client: Any = Field(default=None, exclude=True)  #: :meta private:
    model_name: str = "chatglm_turbo"
    """Model name to use."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Holds any model parameters valid for `create` call not explicitly specified."""
    # When updating this to use a SecretStr
    # Check for classes that derive from this class (as some of them
    # may assume zhipu_api_key is a str)
    zhipuai_api_key: Optional[str] = Field(default=None, alias="api_key")
    """Automatically inferred from env var `ZHIPUAI_API_KEY` if not provided."""
    max_retries: int = 6
    """Maximum number of retries to make when generating."""
    prefix_messages: List = Field(default_factory=list)
    """Series of messages for Chat input."""
    streaming: bool = True
    """Whether to stream the results or not."""
    allowed_special: Union[Literal["all"], AbstractSet[str]] = set()
    """Set of special tokens that are allowed。"""
    disallowed_special: Union[Literal["all"], Collection[str]] = "all"
    """Set of special tokens that are not allowed。"""


    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Build extra kwargs from additional params that were passed in."""
        all_required_field_names = {field.alias for field in cls.__fields__.values()}

        extra = values.get("model_kwargs", {})
        for field_name in list(values):
            if field_name not in all_required_field_names:
                if field_name in extra:
                    raise ValueError(f"Found {field_name} supplied twice.")
                extra[field_name] = values.pop(field_name)
        values["model_kwargs"] = extra
        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        zhipuai_api_key = get_from_dict_or_env(
            values, "zhipuai_api_key", "ZHIPUAI_API_KEY"
        )
        try:
            import zhipuai

            zhipuai.api_key = zhipu_api_key
        except ImportError:
            raise ImportError(
                "Could not import zhipuai python package. "
                "Please install it with `pip install zhipuai`."
            )
        try:
            values["client"] = zhipuai.model_api
        except AttributeError:
            raise ValueError(
                "`zhipuai` has no `model_api` attribute, this is likely "
                "due to an old version of the zhipuai package. Try upgrading it "
                "with `pip install --upgrade zhipuai`."
            )
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling zhipuai API."""
        return self.model_kwargs
