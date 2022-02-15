# Put all helper functions here - W


# This will render different icons based on category type of flash message for example.
def render_flash_msg_icon(category_type):
    match category_type:
        case "primary":
            return "#info-fill"
        case "success":
            return "#check-circle-fill"
        case "warning":
            return "#exclamation-triangle-fill"
        case "danger":
            return "#exclamation-triangle-fill"

def format_currency(value):
    output = "${:,.2f}".format(value)
    return output


def print_something(value):
    output = value + "new"
    return output


def get_first_s3image_url(url):
    url_list = url.split(";")
    print(url_list)
    return url_list[0]

def get_s3_imageurl_list(url):
    url_list = url.split(";")
    return url_list