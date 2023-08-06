import os
import streamlit.components.v1 as components

__all__ = ['sync']

_RELEASE = True

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "sync")
_component_func_send = components.declare_component("sync", path=build_dir)

def sync(
    defaultChecked: bool=False,
    key: str =None) -> str:
    """Create a sync token generator.

    Parameters
    ----------
    defaultChecked: bool
        Set if it has to be checked by default.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    Returns
    -------
    str
        Sync token to connect to component to enable the syncronization.
    """
    component_value = _component_func_send(
        defaultChecked=defaultChecked,
        key=key, 
        default=None)

    return component_value

if not _RELEASE:
    import streamlit as st
    st.subheader("Sync Token in action")

    # just one component like this
    sync_token = sync(defaultChecked=True, 
        key='my-secret-key')
    st.write(sync_token)
    
    sync_token_2 = sync(defaultChecked=True, 
        key='my-secret-key-2')
    st.write(sync_token_2)