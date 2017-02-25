from conf import API_SERVER, GUI_SERVER


def _construct_url(url_object):
    try:
        port = url_object.port
        if int(port) in [80, 443]:
            return "%s://%s" % (
                url_object.protocol,
                url_object.host
            )
    except AttributeError:
        pass

    return "%s://%s:%s" % (
        url_object.protocol,
        url_object.host,
        url_object.port
    )


def get_gui_url():
    """
    Returns the URL to terrene's GUI
    """
    return _construct_url(GUI_SERVER)


def get_api_url():
    """
    Returns the URL to terrene's API
    """
    return _construct_url(API_SERVER)
