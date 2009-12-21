## from __future__ import with_statement
## import os
import pprint

PCD = '#PCDATA'
ELSTART = '<!ELEMENT'
ATTSTART = '<!ATTLIST'
ENTSTART = '<!ENTITY'
END = '>'

def valid_name(name):
    """
    nakijken welke tekens er niet in een naam mogen voorkomen
    voorlopig mag alles
    """
    error_chars = []
    for char in error_chars:
        if char in name:
            return False
    return True

def Element(**argv):
    """
    Create an element definition.
    valid keyword arguments are:
        name (string) - the name of the element
        type (string) - EMPTY or ANY; if neither, do not specify
        occ (string) - number of occurrences: *, + or ?,
            empty or do not specify for 1
        alt (bool) - True for either/or value, else False or do not specify
    returns the created definition

    to modify afterwards, (re)assign the returned item's attributes:
        name
        type
        occurrence
    """
    type = argv.get('type',None)
    is_alternative = argv.get('alt',False)
    if type == PCD[2:]:
        if is_alternative:
            return _Element(name=PCD,occ="",alt=True)
        else:
            return _Element(name=PCD,occ="")
    else:
        return _Element(**argv)

def Attribute(parent,**argv):
    """
    Create an attribute definition.
    valid keyword arguments are:
        name (string) - the name of the attribute
        type (string) - currently implemented: CDATA (default), ID, IDREF, IDREFS
            do not specify for enumerated list of values
        val (string) -  req, impl or fix; dflt or do not specify for default value
        items (list) - one or more data values; do not specify for impl or fix
    returns the created definition

    to modify afterwards, (re)assign the returned item's attributes:
        name
        type
        value_type
        value_list
    """
    child = _Attribute(**argv)
    child.parent = parent
    parent.attribute_list.append(child)
    return child

def Entity(**argv):
    """
    Create an entity definition.
    valid keyword arguments are:
        name (string) - the entity name, i.e. "nbsp" for &nbsp;
        type (string) - 'ent' or do not specify for internal definition,
            'ext' for external dtd
        value (string) - the entity contents or the url to the external dtd
    returns the created definition

    to modify afterwards, (re)assign the returned item's attributes:
        name
        type
        value
    """
    child = _Entity(**argv)
    ## child.parent = parent
    ## parent.entity_list.append(child)
    return child

def SubItem(parent,child=None,**argv):
    """
    Define that a parent contains an element or attribute or entity.
    valid keyword arguments are:
        child (object) - the element, attribute or entity to add
        one or more of the arguments used for Element(),
            as a shortcut to directly add a subelement
    returns the added or created child object

    vraag:
    (test+,(hallo*|empty)) lukt
    maar hoe krijg je (test+|(hallo*|empty)) voor elkaar
    of ((hallo*|empty)|test+)
    """
    child = Element(**argv)
    if child.is_alternative:
        test = parent.subelement_list[-1]
        if isinstance(test,_Altlist):
            test.add(child)
        else:
            new = _Altlist(items=[child,])
            parent.subelement_list.append(new)
    elif isinstance(parent,_Element):
        parent.subelement_list.append(child)
    return child

def Text(parent,alt=False):
    "shortcut to define that an element contains text"
    return SubItem(parent,type=PCD[2:],alt=alt,occ='')

class DTDParsingError(Exception):
    pass

class _Element(object):
    """
    internal representation of an element definition with subordinate objects
    """
    def __init__(self,**argv):
        self.name = argv.get('name',None)
        self.type = argv.get('type','ANY') # EMPTY, ANY, CDATA
        self.occurrence = argv.get('occ',"") # 1, 1-n, 0-1, 0-n
        self.is_alternative = argv.get('alt',False) #
        self.subelement_list = []
        self.attribute_list = []
        self.entity_list = []

    def __setattr__(self, name, value):
        if name == "name":
            if not valid_name(value):
                raise ValueError('illegal value for Element.name')
        elif name == "type":
            if value and value not in ('EMPTY','ANY'):
                raise ValueError('illegal value for Element.type')
        elif name == "occurrence":
            if value and value not in ('','*','+','?'):
                raise ValueError('illegal value for Element.occurrence')
        object.__setattr__(self, name, value)

    def __str__(self):
        me = []
        for item in self.entity_list:
            me.append(str(item))

        if self.subelement_list:
            data = ''
            for item in self.subelement_list:
                if isinstance(item,_Altlist):
                    extra = "|".join([x.name + x.occurrence for x in item._list])
                    extra = extra.join(("(",")"))
                else:
                    extra = item.name + item.occurrence
                if data:
                    data = ','.join((data,extra))
                else:
                    data = extra
            data = data.join(("(",")"))
        else:
            data = self.type
        if self.name != PCD:
            me.append(" ".join((ELSTART,self.name,data)) + END)
        for item in self.subelement_list:
            if str(item) != '':
                me.append(str(item))
        for item in self.attribute_list:
            me.append(str(item))
        return "\n".join(me)

class _Altlist(object):
    """
    helper structure for alternatives under an element
    """
    def __init__(self,**argv):
        self._list = argv.get('items',[])

    def add(self,item):
        self._list.append(item)

class _Attribute(object):
    """
    internal representation of an attribute definition
    """
    atttypes = ('CDATA','ENUM','ID','IDREF','IDREFS',
    ## 'NMTOKEN','NMTOKENS','ENTITY','ENTITIES','NOTATION',
    )
    valtypes = {'dflt':'', 'req': '#REQUIRED', 'impl': '#IMPLIED', 'fix': '#FIXED'}
    def __init__(self,**argv):
        self.name = argv.get('name',None)
        self.type = argv.get('type','CDATA') #  CDATA, ENUM, ID etc.
        self.value_type = argv.get('decl','dflt') #  dflt, req, impl, fix
        self.value_list = argv.get('items',[]) #  (0-n items)
        self.default = argv.get('value','')

    def __setattr__(self, name, value):
        if name == "name":
            if not valid_name(value):
                raise ValueError('illegal value for Attribute.name')
        elif name == "type":
            if value and value not in self.atttypes:
                raise ValueError('illegal value for Attribute.type')
        elif name == "value_type":
            if value and value not in self.valtypes:
                raise ValueError('illegal value for Attribute.valuetype')
        elif name == "default":
            if value and self.value_type and self.value_type == 'impl':
                raise ValueError('illegal value for Attribute.default')
        elif name == "value_list":
            if value and self.type and self.type != 'ENUM':
                raise ValueError('illegal value for Attribute.valuelist')
        object.__setattr__(self, name, value)

    def __str__(self):
        if len(self.value_list) > 1:
            typ = "|".join(self.value_list).join(('(',')'))
            val = ''
        else:
            typ = self.type
            val = self.valtypes[self.value_type]
        if self.value_type in ('dflt','fix') and self.default:
            val = '{0} "{1}"'.format(val,self.default)
        data = " ".join((ATTSTART,self.parent.name,self.name,typ,val))
        return data.strip() + END

class _Entity(object):
    """
    internal representation of an entity definition
    """
    def __init__(self,**argv):
        self.name = argv.get('name',None)
        self.type = argv.get('type','ent') #
        self.value = argv.get('value', '') #

    def __setattr__(self, name, value):
        if name == "name":
            if not valid_name(value):
                raise ValueError('illegal value for Entity.name')
        elif name == "type":
            if value and value not in ('ent','ext'):
                raise ValueError('illegal value for Entity.type')
        object.__setattr__(self, name, value)

    def __str__(self):
        if self.type == 'ent':
            value = self.value.join(('"','"'))
        else:
            value = 'SYSTEM ' + self.value
        return ' '.join((ENTSTART, self.name,value)) + END

class DTDParser(object):
    def __init__(self,dtdfile=None,fromstring=''):
        parse_buf = ""
        line_buf = []
        self._dtd = []
        self._dtd_dic = {}
        self._line = -1
        self._pos = -1
        if dtdfile:
            with open(dtdfile) as invoer:
                line_buf = invoer.readlines()
        elif fromstring:
            line_buf = fromstring.split("\n")
        else:
            raise DTDParsingError("No input provided")
        for line in line_buf:
            self._line += 1
            self._pos = -1
            if line.strip() != "":
                if parse_buf:
                    parse_buf = parse_buf + " "
                parse_buf += line.rstrip()
                test = parse_buf.split(">",1)
                try:
                    self._parse(test[0])
                except DTDParsingError:
                    raise
                self._pos += len(test[0])
                if len(test) > 1:
                    parse_buf = test[1]
                else:
                    parse_buf = ''
        if parse_buf:
            try:
                self._parse(parse_buf)
            except DTDParsingError:
                raise
        self._finalize()

    def _parse(self,buffer):
        print("buffer:",buffer)
        if buffer[:2] != "<!":
            raise DTDParsingError("Illegal statement start at line " + str(self._line))
        test = buffer.split(None,1)
        if test[0] == ELSTART:
            self._parse_element(test[1])
        elif test[0] == ATTSTART:
            self._parse_attribute(test[1])
        elif test[0] == ENTSTART:
            self._parse_entity(test[1])
        else:
            raise DTDParsingError("Illegal keyword in line " + str(self._line))

    def _parse_element(self,inp):
        try:
            name,data = inp.split(None,1)
        except ValueError:
            raise DTDParsingError("Incomplete element definition in line " + str(self._line))
        if name in self._dtd_dic:
            me = self._dtd_dic[name]
        else:
            me = Element(name=name)
            self._dtd_dic[name] = me
            self._dtd.append(me)
        if data.startswith("("):
            if data.endswith(")"):
                data = data[1:-1]
            else:
                raise DTDParsingError("Element definition error: unbalanced parentheses in line " + str(self._line))
        while data:
            if data.startswith('('):
                test = data.split(')',1)
                alt = _Altlist()
                for item in test[0][1:].split('|'):
                    new = Element(name=item)
                    self._dtd_dic[item] = new
                    alt.add(el)
                SubItem(me,alt)
                if len(test) > 1:
                    if test[1].startswith(','):
                        data = test[1][1:]
                        if data == '':
                            raise DTDParsingError("Unfinished element definition in line " + str(self._line))
                    else:
                        data = test[1]
                else:
                    data = ''
            else:
                test = data.split(',',1)
                new = SubItem(me,name=test[0])
                self._dtd_dic[test[0]] = new
                data = '' if len(test) == 1 else test[1]

    def _parse_attribute(self,inp):
        try:
            parent,data = inp.split(None,1)
            print("parent:",parent)
            while data:
                name,data = data.split(None,1)
                print("name:",name)
                if data.startswith("("):
                    ix = data.find(')')
                    print("ix:",ix)
                    if ix == -1:
                        raise DTDParsingError('Incorrect attribute definition')
                    enum,data = data.split(")",1)
                    enum = enum[1:].split('|')
                    print("enum",enum)
                    data = data.lstrip()
                    print("data:",data)
                    if data.startswith('"'):
                        ix = data[1:].find('"')
                        if ix == -1:
                            raise DTDParsingError('Incorrect attribute definition')
                        decl = 'dflt'
                        item = data[1:ix+1]
                        print("item:",item)
                        data = data[ix+2:].lstrip()
                        print("data:",data)
                    else:
                        decl,data = data.split(None,1)
                    new = Attribute(self._dtd_dic[parent],name=name,
                        type = "ENUM",decl=decl,items=enum,value=item)
                    if len(data) > 1:
                        data = data[1]
                else:
                    type,decl,data = data.split(None,2)
                    print("type:",type)
                    if decl == '#FIXED':
                        value,data = data.split(None,1)
                        new = Attribute(self._dtd_dic[parent],name=name,
                            type = type,decl='fix',value=item)
                    elif decl.startswith('"'):
                        if decl.endswith('"'):
                            new = Attribute(self._dtd_dic[parent],name=name,
                                type = type,decl='dflt',value=decl[1:-1])
                        else:
                            raise DTDParsingError('Incorrect attribute definition')
                    else:
                        if decl == '#REQUIRED':
                            decl = 'req'
                        elif decl == '#IMPLIED':
                            decl = 'impl'
                        else:
                            raise DTDParsingError('Incorrect attribute definition')
                        new = Attribute(self._dtd_dic[parent],name=name,
                            type = type,decl=decl)
        except ValueError:
            raise DTDParsingError('Incorrect attribute definition')

    def _parse_entity(self,inp):
        try:
            name,data = inp.split(None,1)
        except ValueError:
            raise DTDParsingError("Incomplete entity definition in line " + str(self._line))
        type = ''
        if data.startswith('"') and data.endswith('"'):
            type = 'ent'
        elif data.startswith("SYSTEM"):
            data = data.split(None,1)
            if len(data) > 1:
                if data[1].startswith('"') and data[1].endswith('"'):
                    data = data[1]
                    type = 'ext'
        if type:
            me = Entity(name=name,type=type,value=data[1:-1])
            self._dtd.append(me)
        else:
            raise DTDParsingError("Incomplete entity definition in line " + str(self._line))

    def _finalize(self):
        # replace placeholders (element names) with actual elements
        pass

    def __str__(self):
        me = []
        for item in self._dtd:
            me.append(str(item))
        return "\n".join(me)

def test_build_dtd():
    ## no_1 = Element(name='top')
    ## no_2 = SubItem(no_1,type="PCDATA")
    ## no_3 = SubItem(no_1,name="hallo",alt=True)
    ## no_4 = SubItem(no_1,name="empty",type='EMPTY',occ='',alt=True)
    ## print no_1
    ## print no_2
    ## print no_3
    ## print no_4
    email = Element(name='email')
    sender = SubItem(email,name='from',occ="")
    Text(sender)
    dest = SubItem(email,name='to',occ="")
    Text(dest)
    title = SubItem(email,name='subject',occ="")
    Text(title)
    body = SubItem(email,name='text',occ="")
    Attribute(body,name='words',val='dflt',default='0')
    Attribute(body,name='type',type='ENUM',items=['0','1','2'],value='0')
    hlp = Attribute(body,name='checked')
    Text(body)
    Entity(name="stfu",value="stuffit")
    return email

def test_parse_dtd():
    email = ""
    try:
        email = DTDParser(fromstring="""\
<!ELEMENT note (to,from,heading,body)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT heading (#PCDATA)>
<!ELEMENT body (#PCDATA)>
<!ATTLIST body NAME CDATA #IMPLIED CATEGORY (HandTool|Table|Shop-Professional) "HandTool" PARTNUM CDATA #IMPLIED PLANT (Pittsburgh|Milwaukee|Chicago) "Chicago" INVENTORY (InStock|Backordered|Discontinued) "InStock">
<!ENTITY writer "Donald Duck.">
<!ENTITY copyright SYSTEM "http://www.w3schools.com/entities.dtd">
""")
    except DTDParsingError as msg:
        print(msg)
    return email

def main():
    ## print test_build_dtd()
    ## print
    print(str(test_parse_dtd()))
    #raw_input()

if __name__ == "__main__":
    main()