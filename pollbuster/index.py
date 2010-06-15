def main():
    try:
        fp = open( "pollbuster.tpl" )
        tpl = fp.read()
    except (IOError, OSError):
        tpl = "{content}"

    content = "meukzooi";

    output = tpl.replace( "{content}", content.encode( "utf-8" ) )
    print "Content-Type: text/html"
    print "Content-Length:", len(output)
    print
    print output

if __name__ == "__main__":
    main()
