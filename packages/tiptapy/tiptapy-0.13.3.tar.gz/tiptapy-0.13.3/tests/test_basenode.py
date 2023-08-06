from tiptapy import renderers


def _test_textnode():
    renderer = renderers.get('text')
    out = renderer.render({'type': 'text', 'text': 'text content'})
    print(out)
