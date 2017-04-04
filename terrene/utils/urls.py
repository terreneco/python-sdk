from terrene.conf import API_SERVER, GUI_SERVER


def _construct_url(url_object):
    """
    Args:

    Returns:
        a string in format `protocol://host:port`

    Raises:
        None
    """
    try:
        port = url_object.get('port')
        if int(port) in [80, 443]:
            return "%s://%s" % (
                url_object.get('protocol'),
                url_object.get('host')
            )
    except AttributeError:
        pass

    return "%s://%s:%s" % (
        url_object.get('protocol'),
        url_object.get('host'),
        url_object.get('port')
    )


def get_gui_url():
    """
    Args:

    Returns:
        a string in format `protocol://host:port`

    Raises:
        None
    """
    return _construct_url(GUI_SERVER)


def get_api_url():
    """
    Args:

    Returns:
        a string in format `protocol://host:port`

    Raises:
        None
    """
    return _construct_url(API_SERVER)
