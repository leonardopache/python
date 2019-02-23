from bs4 import BeautifulSoup
import urllib.request



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )

        return s[start:end]

    except ValueError:
        return ""

def read_htlm(url):

    new_url= 'file:///'+url+'/frame-summary.html'


    with urllib.request.urlopen(new_url) as response:
        html = response.read()

    html_formatted = BeautifulSoup(html, 'html.parser')


    tag_span=html_formatted.find_all('span')

    line_node = str(tag_span[0])
    branch_node = str(tag_span[1])

    if line_node.find('N/A') != -1:
        lines_covered = 'N/A'
        lines_total = 'N/A'
    else:
        get_lines= find_between(line_node,'>','<').split('/')
        lines_covered= str(get_lines[0])
        lines_total= str(get_lines[1])


    if branch_node.find('N/A') != -1:
        branch_covered = 0
        branch_total = 0
    else:
        get_branch = find_between(branch_node,'>','<').split('/')
        branch_covered= str(get_branch[0])
        branch_total= str(get_branch[1])

    print("lines covered: %s | lines total: %s \nbranches covered: %s | branches total: %s"
          % (lines_covered,lines_total,branch_covered,branch_total))

    return (lines_covered,lines_total,branch_covered,branch_total)




