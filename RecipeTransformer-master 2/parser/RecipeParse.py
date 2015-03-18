import json
from bs4 import BeautifulSoup
import urllib2
from textblob import TextBlob
import codecs
from fractions import Fraction

# Example urls.
# Refer to bottom of file for running parser.
# TODO: clean up comments and code

url_example = 'http://allrecipes.com/recipe/worlds-best-lasagna/'   # lasagna recipe for testing
url_jambalaya ='http://allrecipes.com/recipe/jambalaya/'            # jambalaya recipe for testing
url_chicken = 'http://allrecipes.com/Recipe/Shepherds-Pie/Detail.aspx?event8=1&prop24=SR_Thumb&e11=shepherd%20pie&e8=Quick%20Search&event10=1&e7=Recipe&soid=sr_results_p1i2'

#testing purposes only
html = urllib2.urlopen(url_example).read()
soup1 = BeautifulSoup(html)



def startParse():
	
	print "Running Recipe Parse..."
	url_enter = raw_input("Enter valid URL ALLRECIPE: ")
	
	RecipeParse(str(url_enter))
	RecipeParseToJson(str(url_enter),"recipedata.txt")
	
	return 


########################
# Pre-process code
########################

def fetchURL(url):
    """
    return html page of passed url.
    :param url: string of url/address
    :return soup: html formatted by beautifulsoup
    """
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup







###############
# Scraping code
###############

def fetchRecipeName(soup):
    """
    return recipe name/title of html soup
    :param soup: html soup
    :return name: name of recipe
    """
    name = soup.find("h1",{"itemprop":"name"})
    return name.text


def amountFetch(soup):
    """
    scrape and return general amounts for each ingredients.
    """
    amt = [link.text for link in soup.find_all("span",{"class":"ingredient-amount"})]
    return amt


def quantityFetch(soup):
    """
    Returns quantity of each ingredient as a float.
    :param soup: html
    :return qnum: quantity
    """
    qft = [link.text for link in soup.find_all("span",{"class":"ingredient-amount"})]
    qdata = []
    qnum=[]

    for integer in range(0,len(qft)):
        qsplit = "".join(qft[integer]).split(' ')
        qdata.append(qsplit)

    for integer in range(0,len(qdata)):
        acc = float(0);
        x = qdata[integer]
        for integer in range(0,len(x)):


            if(x[integer].isdigit()):
                new_q=float(sum(Fraction(s) for s in x[integer].split()))
                acc += new_q
                #print new_q

            elif("/" in x[integer]):
                frac_to_float=float(sum(Fraction(s) for s in x[integer].split()))
                acc += frac_to_float
                #print frac_to_float

        qnum.append(acc)
    return qnum


def mmUnitFetch2(soup):
    qft = [link.text for link in soup.find_all("span",{"class":"ingredient-amount"})]
    qdata = []
    qnum=[]
    return qft



def mmUnitFetch(soup):
    qft = [link.text for link in soup.find_all("span",{"class":"ingredient-amount"})]
    qdata = []
    qnum=[]

    for integer in range(0,len(qft)):
        qsplit = "".join(qft[integer]).split(' ')
        qdata.append(qsplit)

    for integer in range(0,len(qdata)):
        acc = float(0);
        x = qdata[integer]
        for integer in range(0,len(x)):

            if(len(x)==1):
                qnum.append("none")

            if(x[integer].isdigit()):
                new_q=float(sum(Fraction(s) for s in x[integer].split()))
                acc += new_q

            elif("/" in x[integer]):
                frac_to_float=float(sum(Fraction(s) for s in x[integer].split()))
                acc += frac_to_float

            elif("(" in x[integer]):
                comb1 = "".join(x[integer])
                comb2 = "".join(x[integer+1])
                comb3 = "".join(x[integer+2])
                comb4 = comb1+comb2+comb3
                qnum.append(comb4)

            elif(")" in x[integer]):
                qnum.append("none")
                
            else:
                qnum.append(x[integer])
                None

    return qnum




def ingredientFetch(soup):
    """
    scrape html text that relate to ingredient name
    """
    ift = [link.text for link in soup.find_all("span",{"class":"ingredient-name"})]
    return ift



def ratingFetch(soup):
    """
    scrape recipe ratings
    """
    ratings=soup.find("meta", {"itemprop":"ratingValue"})['content']
    return ratings


def directionFetch(soup):
    """
    scrape list of directions/steps
    returns sentences
    """
    list_directions = soup.find("ol").text
    zen = TextBlob(list_directions)
    tokenDirection=zen.sentences
    return tokenDirection


def directionString(soup):
    """scrape and return string of directions
    """
    list_directions = soup.find("ol").text
    zen = "".join(list_directions)
    tokenDirection = zen.split(".")
    return tokenDirection


# Nutrition Scrape code

def mineCalories(soup):
    kcal=soup.find("li",{"class":"units"}).text
    return kcal



#################
# Processing code
#################

def mProcess(soup):
    """
    Returns measurement information from list of ingredients.
    :param soup:
    :return:

    """
    mdata = ingredientProcess(soup);
    for integer in range(0,16):
        print mdata[integer]

    x=mdata[0]
    mp=x.split("\n")
    return mp

def ingredientProcess(soup):
    """
    Returns list of ingredients scraped from the soup.

    :param soup:
    :return f_data: list of ingredients
    """
    ingredient_data = [link.text for link in soup.find_all("ul",{"class":"ingredient-wrap"})]
    ingredient_string = "".join(ingredient_data)
    struct_ingre=ingredient_string.split("\n\n\n")
    i_data= filter(None,struct_ingre)
    s_data = "".join(i_data).split("\n\n")
    f_data =filter(None,s_data)

    for integer in range(0,len(i_data)):
        if i_data[integer] == "\n":
            del i_data[integer]

    return i_data





def ingredientCheck(soup):

    raw_list = []
    q_list = []
    unit_list=[]
    unit_list = mmUnitFetch2(soup)
    final_list = []
    raw_list = ingredientProcess(soup)
    q_list = quantityFetch(soup)

    for integer in range(0,len(raw_list)):

        if num_there(str(raw_list[integer])):
            None
        else:
             q_list.insert(integer,"none")
             unit_list.insert(integer,"none")

    return q_list


def ingredientCheckUnit(soup):

    raw_list = []
    q_list = []
    unit_list=[]
    unit_list = mmUnitFetch2(soup)
    final_list = []
    raw_list = ingredientProcess(soup)
    q_list = quantityFetch(soup)

    for integer in range(0,len(raw_list)):
        if num_there(str(raw_list[integer])):
            None
        else:
             q_list.insert(integer,"none")
             unit_list.insert(integer,"none")
    return unit_list
    
    
    
def ingredientCheckUnit3(soup):

    raw_list = []
    q_list = []
    unit_list=[]
    unit_list = mmUnitFetch2(soup)
    final_list = []
    raw_list = ingredientProcess(soup)
    q_list = quantityFetch(soup)

    for integer in range(0,len(raw_list)):
        if num_there(str(raw_list[integer])):
            None
        else:
             q_list.insert(integer,"none")
             unit_list.insert(integer,"none")
             
             
             
             
	mod_lst = []
	
	for integer in range(0,len(unit_list)):
		if num_there(str(unit_list[integer])):
			if (len(unit_list[integer])==1):
				mod_lst.append("none")
				
			elif("/" in unit_list[integer]):
				str1 = "".join(unit_list[integer])
				mod_lst.append(str1[4:len(str1)])
			
			else: 
				str1 = "".join(unit_list[integer])
				mod_lst.append(str1[2:len(str1)])
			
		else: 
			mod_lst.append(unit_list[integer])
    return mod_lst
    

	


def num_there(s):
    return any(i.isdigit() for i in s)


def prepareProcess(soup):

    pft = ingredientFetch(soup)
    result_data = []
    for integer in range(0,len(pft)):
        if (',' in pft[integer]):

            x = "".join(pft[integer]).split(',')
            result_data.append(x[1])
        else:
            result_data.append("none")
    return result_data

def ingredientnameProcess(soup):
    pft = ingredientFetch(soup)
    resultdata = []

    for integer in range(0,len(pft)):
        if (',' in pft[integer]):

            x = "".join(pft[integer]).split(',')
            resultdata.append(x[0])
        else:
            resultdata.append(pft[integer])
    return resultdata


def getDirection(id, soup):
    """
    retrieve specific direction via index of list.
    """
    stor=[]
    stor=directionFetch(soup)
    id = stor[id-1]
    return id



###############
# Parser code
###############

def RecipeParseToJson(url, outpath):
    """
    Writes a json file containing parsed recipe from html page.
    :param url: url of recipe, must be an ALLRECIPE.COM url
    :return void
    """

    outfile = RecipeParse(url)

    with codecs.open(outpath,"w","utf-8") as f:
        print "Writing to ", outpath
        f.write(json.dumps(outfile, indent=4))


def RecipeParse(url):
    """
    Writes a json file containing parsed recipe from html page.
    :param url: url of recipe, must be an ALLRECIPE.COM url
    :return void
    """
    
    soup = fetchURL(url)
    list_format = ["name","quantity","measurement","descriptor","preparation","prep-description"]

    n_data = ingredientnameProcess(soup)
    m_data = ingredientCheckUnit3(soup)
    p_data = prepareProcess(soup)
    q_data = ingredientCheck(soup)
    

    out_dict=[]
    i_dict={}
    library_dict=[]

    for integer in range(0,len(n_data)):
        nlist = [n_data[integer],q_data[integer],m_data[integer],["".join(n_data[integer]).split(" ")],p_data[integer],"none"]
        out_dict.append(nlist)

    for integer in range(0,len(n_data)):
        library_dict.append(dict(zip(list_format,out_dict[integer])))

    parsed_recipe = {
        "Info":{
            "recipe":fetchRecipeName(soup),
            "rating":ratingFetch(soup),
        },
        "ingredients":library_dict,
        "steps":directionString(soup),
        #tools":{},
        #methods":{},
        "nutrition":{
        "calories":mineCalories(soup)
        }
    }

    return parsed_recipe
    
    
    
    


#RecipeParseToJson(url_example,"recipedata.txt")

#startParse()