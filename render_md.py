import os
from datetime import datetime
import time
import markdown

BASE_TEMPLATE = 'template.html'
ROOT_DIR = '.'

REFRESH_JS = '<script type="text/javascript">setInterval("window.location.reload()", 2 * 1000);</script>'

def recursive_render(rootdir='.', refresh=False):
    template = open(BASE_TEMPLATE).read()
    if refresh:
        ref_script = REFRESH_JS
    else:
        ref_script = ''

    md = markdown.Markdown(extensions=['markdown.extensions.toc',
                                       'markdown.extensions.tables',
                                       'markdown.extensions.codehilite'])
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.md'):
                print(os.path.join(root,file))
                with open(os.path.join(root,file)) as f:
                    html = md.convert(f.read())
                with open(os.path.join(root, file + '.html'), 'w') as f:
                    f.write(template.format(html, ref_script))


def check_modified_closure():
    last_check = datetime(year=2000, month=1,day=1)
    print("init...")

    def inner(rootdir='.'):
        nonlocal last_check
        for root, dirs, files in os.walk(rootdir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root,file)
                    mtime = os.path.getmtime(path)
                    lastmod = datetime.fromtimestamp(mtime)
                    if lastmod > last_check:
                        last_check = datetime.now()
                        return True
        
        last_check = datetime.now()
        return False
    return inner

check_modified = check_modified_closure()
    
def main():
    while True:
        try:
            if check_modified(ROOT_DIR):
                print("Modification detected...")
                recursive_render(ROOT_DIR, refresh=True)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Final render...")
            recursive_render(ROOT_DIR, refresh=False)
            exit(0)

if __name__ == '__main__':
    main()
