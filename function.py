import re

def getClosestMatch(listInput, searchQuery):

    estimationCutoffValue = 50

    dictOfKeys = {}
    listOfKeys = []

    for keyName in listInput:

        caseNonsensitiveKeyname = keyName.upper()

        dictOfKeys[caseNonsensitiveKeyname] = keyName
        listOfKeys.append(caseNonsensitiveKeyname)

    try:
        searchQueryCleaned = (str(searchQuery).strip()).upper()
    except:
        return [False, False, f"Search query not valid: {searchQuery}"]


    lengthOfSearchQuery = len(searchQueryCleaned)
    anySnip = r"(.*?)"
    pointOfEstimation = int((int((estimationCutoffValue / 10)*lengthOfSearchQuery))/10)


    theInput = re.escape(searchQueryCleaned)
    regexTerm = f"^{anySnip}{theInput}{anySnip}$"
    regex = re.compile(regexTerm)

    theInput = re.escape(searchQueryCleaned[:pointOfEstimation])
    regexTermFirst = f"^{anySnip}{theInput}{anySnip}$"
    regexFirst = re.compile(regexTermFirst)

    theInput = re.escape(searchQueryCleaned[lengthOfSearchQuery - pointOfEstimation:])
    regexTermLast = f"^{anySnip}{theInput}{anySnip}$"
    regexLast = re.compile(regexTermLast)

    allMatches = list(filter(regex.match, dictOfKeys.keys()))
    allMatchesFirst = list(filter(regexFirst.match, dictOfKeys.keys()))
    allMatchesLast = list(filter(regexLast.match, dictOfKeys.keys()))

    if searchQueryCleaned in listOfKeys:
        targetKey = dictOfKeys[searchQueryCleaned]

    elif len(allMatches) == 1:
        targetKey = dictOfKeys[allMatches[0]]

    elif len(allMatchesFirst) == 1:
        targetKey = dictOfKeys[allMatchesFirst[0]]
        
    elif len(allMatchesLast) == 1:
        targetKey = dictOfKeys[allMatchesLast[0]]

    else:
        targetKey = None

    if targetKey:
        return [True, True, targetKey]

    else:

        if len(allMatches) > 0:

            closeMatches = []

            for closeMatch in allMatches:
                closeMatches.append(dictOfKeys[closeMatch])
            
            return [True, False, closeMatches]

        else:
            return [True, False, []]
