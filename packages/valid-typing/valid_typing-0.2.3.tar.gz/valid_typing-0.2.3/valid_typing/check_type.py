import typing


def check_type(actual, definition):
    # Currently any type variable will be considered generic
    if type(definition) == typing.TypeVar:
        return True

    # Any allows any.
    if definition == typing.Any:
        return True

    try:
        actual_origin = actual.__origin__
    except AttributeError:
        actual_origin = actual
        actual_args = tuple()
    else:
        actual_args = typing.get_args(actual)

    try:
        definition_origin = definition.__origin__
    except AttributeError:
        definition_origin = definition
        definition_args = tuple()
    else:
        definition_args = typing.get_args(definition)

    if actual_origin == typing.Union:
        return all(check_type(arg, definition) for arg in actual_args)

    if definition_origin == typing.Union:
        return any(check_type(actual, arg) for arg in definition_args)

    try:
        # For the case where typing.Iterable is good for typing.List
        class_similarity = issubclass(actual_origin, definition_origin)
    except TypeError:
        class_similarity = actual_origin == definition_origin

    if actual == str:
        # For how we're testing, a `str` is technically an iterable that has the element type of `str`
        actual_args = (str,)

    if definition == str:
        # For how we're testing, a `str` is technically an iterable that has the element type of `str`
        definition_args = (str,)

    return (
        class_similarity
        and len(actual_args) >= len(definition_args)
        and (
            actual_args == definition_args
            or all(
                check_type(actual_args[i], definition_args[i])
                for i in range(len(definition_args))
            )
        )
    )
