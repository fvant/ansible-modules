
def sprintf(string, format_str):
    return format_str.format( *string.split() ) 


class FilterModule(object):

    def filters(self):
        return {
            'sprintf': sprintf
        }
