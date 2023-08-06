"""Utility functions and common classes."""

import re
from dataclasses import dataclass
from inspect import get_annotations
from typing import Generic, Type, TypeVar, get_args, get_origin

def camel_snake_converter(string: str, snake_to_camel: bool = False):
    """
    Converts camel case strings to snake case strings, and vice-versa.
    
    Parameters:
        `string`: The string to be converted
        `snake_to_camel`: Determines which way to convert. \
            Default value will convert camel case to snake case.
    
    Returns:
        The converted string.
    """
    if snake_to_camel:
        snakes: list[str] = re.findall(r"_[a-z]", string)
        replacements = [x.upper()[1] for x in snakes]
        for s, r in zip(snakes, replacements):
            string = string.replace(s, r)
        return string
    else:
        capitals: list[str] = re.findall(r"[A-Z]", string)
        replacements = [f"_{x.lower()}" for x in capitals]
        for c, r in zip(capitals, replacements):
            string = string.replace(c, r)
        return string

T = TypeVar('T')
def assign_response_dict_to_class(resource: dict, cls: Type[T]):
    """
    Takes a class and a resource, and converts that resource into an object.
    
    Parameters:
        `resource`: the resource to be converted.
        `cls`: the class whose object is to be converted into.
    
    Returns:
        An instance of type `cls`, whose attrs are filled with values from `resource`.
    """
    inst: T = cls() # creates an instance of the class.
    # get all the annotations from inherited classes
    for x in cls.__bases__:
        if "__annotations__" in x.__dict__:
            inst.__annotations__.update(x.__annotations__)
    
    for (attr, typ) in inst.__annotations__.items():
        # goes thru the attrs and the annotations of the attrs. 
        converted = camel_snake_converter(attr, True) # converts class attrs to resource keys
        if resource and resource.get(converted):
            if typ in {str, int, bool, list[str], list[int], list[bool]}:
                # * if the attr is a "simple" type, a type we can just copy from the resource directly
                # * just copy it from the resource directly (converting cases first)
                inst.__setattr__(attr, resource[converted])
            elif get_origin(typ) == list:
                # * if the attr is a complex type within a list
                # * go thru the list, and apply the same process as the case down there
                # * just appending to the list this time
                # * then you finally assign the list to the attr. (maybe)
                ls = [] 
                for x in resource.get(converted):
                    ls.append(assign_response_dict_to_class(x, get_args(typ)[0]))
                inst.__setattr__(attr, ls)
            else:
                # * if the attr is a "complex" type, on which has it's own values
                # * use this fuction on it's annontation to convert the resource to an obj
                # * then assign it back to the attr
                # * this process works recursively
                inst.__setattr__(attr, assign_response_dict_to_class(resource.get(converted), 
                                                                     typ))
        else:
            inst.__setattr__(attr, None)
    return inst

@dataclass
class ResponseResourceBase:
    """Base class for all resource and response representations."""
    kind: str = None
    etag: str = None
    dict: dict = None
    
    @classmethod
    def _from_response_dict(cls, response: dict):
        inst = assign_response_dict_to_class(response, cls)
        inst.dict = response
        return inst

@dataclass
class PageInfo:
    total_results: int = None
    results_per_page: int = None
    
@dataclass
class ListResponse(ResponseResourceBase, Generic[T]):
    next_page_token: str = None
    prev_page_token: str = None
    page_info: PageInfo = None
    items: list[T] = None
    
def create_list_response(typ: type[T]) -> type[ListResponse[T]]:
    """
    Creates a parameterized `ListResponse`, with a parameterized `items` attr.
    
    Parameters:
        typ: the type that the return value will be parameterized by.
        
    Returns:
        A ListResponse parameterized by typ. This type parameter is the same type
        as the type parameter of the `list` of the `items` attr.
    """
    
    # clones `ListResponse` 
    class Internal(ListResponse): pass 
    # changes the type annotation of the clone
    anno = get_annotations(ListResponse) 
    anno['items'] = list[typ]
    Internal.__annotations__ = anno
    # get all the annotations from ListResponse's inherited classes
    for x in ListResponse.__bases__:
        if '__annotations__' in x.__dict__:
            Internal.__annotations__.update(x.__annotations__)
            
    return Internal
