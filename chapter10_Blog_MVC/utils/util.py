def truncate_text(text, limit=150) -> str :
    print('text length : ', len(text))
    if text is not None :
        if len(text) > limit :
            truncate_text = text[:limit] + '...'
        else :
            truncate_text = text
        return truncate_text
    return None

def newline_to_br(text_newline : str)  -> str :
    if text_newline is not None :
        return text_newline.replace('\n', '<br>')
    return None

