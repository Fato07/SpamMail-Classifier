from email import message_from_file
import os
import sys


def construct_name(id, fn):
    """Constructs a file name out of messages ID and packed file name"""
    id = id.split(".")
    id = id[0] + id[1]
    return id + "." + fn


def file_exists(f):
    """Checks whether extracted file was extracted before."""
    return os.path.exists(os.path.join(path, f))


def save_file(fn, cont):
    """Saves cont to a file fn"""
    file = open(os.path.join(path, fn), "wb")
    file.write(cont)
    file.close()


def disgra(s):
    """Removes < and > from HTML-like tag or e-mail address or e-mail ID."""
    s = s.strip()
    if s.startswith("<") and s.endswith(">"): return s[1:-1]
    return s


def disqo(s):
    """Removes double or single quotations."""
    s = s.strip()
    if s.startswith("'") and s.endswith("'"): return s[1:-1]
    if s.startswith('"') and s.endswith('"'): return s[1:-1]
    return s


def pullout(m, key):
    """Extracts content from an e-mail message.
    This works for multipart and nested multipart messages too.
    m   -- email.Message() or mailbox.Message()
    key -- Initial message ID (some string)
    Returns tuple(Text, Html, Files, Parts)
    Text  -- All text from all parts.
    Html  -- All HTMLs from all parts
    Files -- Dictionary mapping extracted file to message ID it belongs to.
    Parts -- Number of parts in original message.
    """
    Html = ""
    Text = ""
    Files = {}
    Parts = 0
    if not m.is_multipart():
        if m.get_filename():  # It's an attachment
            fn = m.get_filename()
            cfn = construct_name(key, fn)
            Files[fn] = (cfn, None)
            if file_exists(cfn):
                return Text, Html, Files, 1
            save_file(cfn, m.get_payload(decode=True))
            return Text, Html, Files, 1
        # Not an attachment!
        # See where this belongs. Text, Html or some other data:
        cp = m.get_content_type()
        if cp == "text/plain":
            Text += m.get_payload()
        elif cp == "text/html":
            Html += m.get_payload()
        else:
            # Something else!
            # Extract a message ID and a file name if there is one:
            # This is some packed file and name is contained in content-type header
            # instead of content-disposition header explicitly
            cp = m.get("content-type")
            try:
                id = disgra(m.get("content-id"))
            except:
                id = None
            # Find file name:
            o = cp.find("name=")
            if o == -1: return Text, Html, Files, 1
            ox = cp.find(";", o)
            if ox == -1: ox = None
            o += 5;
            fn = cp[o:ox]
            fn = disqo(fn)
            cfn = construct_name(key, fn)
            Files[fn] = (cfn, id)
            if file_exists(cfn): return Text, Html, Files, 1
            save_file(cfn, m.get_payload(decode=True))
        return Text, Html, Files, 1
    # This IS a multipart message.
    # So, we iterate over it and call pullout() recursively for each part.
    y = 0
    while 1:
        # If we cannot get the payload, it means we hit the end:
        try:
            pl = m.get_payload(y)
        except:
            break
        # pl is a new Message object which goes back to pullout
        t, h, f, p = pullout(pl, key)
        Text += t;
        Html += h;
        Files.update(f);
        Parts += p
        y += 1
    return Text, Html, Files, Parts


def extract(msgfile, key):
    """Extracts all data from e-mail, including From, To, etc., and returns it as a dictionary.
    msgfile -- A file-like readable object
    key     -- Some ID string for that particular Message. Can be a file name or anything.
    Returns dict()
    Keys: from, to, subject, date, text, html, parts[, files]
    Key files will be present only when message contained binary files.
    For more see __doc__ for pullout() and caption() functions.
    """
    m = message_from_file(msgfile)
    From, To, Subject, Date = caption(m)
    Text, Html, Files, Parts = pullout(m, key)
    Text = Text.strip();
    Html = Html.strip()
    msg = {"subject": Subject, "from": From, "to": To, "date": Date,
           "text": Text, "html": Html, "parts": Parts}
    if Files: msg["files"] = Files
    return msg


def caption(origin):
    """Extracts: To, From, Subject and Date from email.Message() or mailbox.Message()
    origin -- Message() object
    Returns tuple(From, To, Subject, Date)
    If message doesn't contain one/more of them, the empty strings will be returned.
    """
    Date = ""
    if "date" in origin:
        Date = origin["date"].strip()
    From = ""
    if "from" in origin:
        From = origin["from"].strip()
    To = ""
    if "to" in origin:
        To = origin["to"].strip()
    Subject = ""
    if "subject" in origin:
        Subject = origin["subject"].strip()
    return From, To, Subject, Date



if __name__ == '__main__':
    path = './ScamMails'
    eml_list = []
    blackList_eml_addresses = ['"Euro-Millions.com" <verification@euro-millions.com>',
                               'Euromillions with Streamail <info@est.zebozut.com>',
                               'XE Money Transfer via Streamail <info@infor.sasonud.eu>',
                               'Webull <noreply@mail.webull.com>',
                               'iFlirts <service@info.iflirts.com>',
                               '=?utf-8?q?The_Compensation_Experts=C2=AE_with_Streamail?= <info@form.furosoyu.com>',
                               'sasi21 <service@crm.mydates.com>',
                               'Mail Delivery System <Mailer-Daemon@server.tempmailgen.com>',
                               'Euromillion Draw with Streamail <info@news.zadeput.com>',
                               '=?utf-8?q?The_Compensation_Experts=C2=AE_with_Streamail?= <info@est.3dflashworld.com>',
                               '"WarbyParker Promo" <wrbp44223@3ab61jnp01oogr.w8591-c42f.vcouzwmu.ga>']

    for files in os.listdir(path):
        if os.path.isfile(os.path.join(path, files)):
            eml_list.append(files)

    sys.stdout = open('overView.txt', 'wt')
    print("{:<70} {:<15} ".format('Emails', 'Results'));
    for eml_file in eml_list:
        f = open(path + "/" + eml_file, 'r')
        s = extract(f, f.name)
        # print(s)

        if s["from"] in blackList_eml_addresses:
            print(eml_file + ": " + "It is a spam")
        else:
            print(eml_file + ": " + "It is not a spam")

