from enum import Enum

from .exceptions import SchemaException


class Initialiser():
    def __init__(self):
        self.context = {
            "entities": [],
            "intents": [],
            "dialogs": [],
            "messages": [],
            "relations": [],
            "subConversationPath": {},
            "conversationId":""
        }

        intents = []
        entities = []
        messages = []
        subConversationPath = {}
        relations = []

class Schemas():


    @staticmethod
    def validateSchema(schema,schemaType= "intents"):
        if schemaType == "intents":
            """

            Intent Schema validation

            """

            if type(schema) != dict:
                raise SchemaException("Intent Samples", "",
                                      "Intents should be a dict of the schema : \n " +
                                      "{\n 'IntentName1' : list of str  ,\n 'IntentName2' : list of str \n " + "}"

                                      )

            for intentName in schema.keys():
                if "_" in intentName:
                    raise SchemaException("Intent", intentName, "Intent Name should not contain '_'  .")

                intentExamples = schema[intentName]

                if type(intentExamples) != list:
                    raise SchemaException("Intent", intentName,
                                          "Intent should be a list of type str , instead intent is {0} .".format(
                                              type(intentExamples)))

                for i, intentSample in enumerate(intentExamples):
                    if type(intentSample) != str:
                        raise SchemaException("Intent", intentName,
                                              "Intent should be a list of type str ,instead intent sample no {0} ({1}) is {2} .".format(
                                                  i, intentSample, type(intentSample)))

            intentNames = schema.keys()
            if "Irrelevant" not in intentNames:
                raise SchemaException("Intent Samples", "No intent with the name Irrelevant .",
                                      "Every bot should have an intent with the name 'Irrelevant' , not found in detected intent names .")
        elif schemaType =="entities":
            if type(schema) != dict:
                # check if entity is dict
                raise SchemaException("Entities", "Entity samples",
                                      "Entities should be specified as a dict instead got  {0} .".format(type(schema)))

            for entityName in schema.keys():
                entityContent = schema[entityName]
                if type(entityContent) != dict:
                    raise SchemaException("Entity", entityName,
                                          "Entities should be specified as a dict instead got  {0} .".format(
                                              type(entityContent)))
                for entitySynonym in entityContent.keys():
                    synonymContent = entityContent[entitySynonym]
                    if type(synonymContent) != list:
                       raise SchemaException("Entity","{0} - {1}".format(entityName,entitySynonym),"Should be a list of dicts instead got {0} of {1}".format(synonymContent,type(synonymContent))

                                             )
                    for i,synonymDefinition in enumerate(synonymContent):
                        if type(synonymDefinition) != dict:
                            raise SchemaException("Entity","{0} - {1}- index {2}".format(entityName,entitySynonym,i),"Should be a dict got {0} of {1}".format(synonymDefinition,type(synonymDefinition))

                                             )
                        for key in synonymDefinition.keys():
                            if key == 'tag':
                                value = synonymDefinition[key]
                                if value not in ["case-insensitive","case-sensitive"]:
                                    raise SchemaException("Entity","{0} - {1}- index {2}".format(entityName,entitySynonym,i),"allowed 'tag' values in ['case-insensitive','case-sensitive'] got {0}".format(value))
                            if key == "type":
                                value = synonymDefinition[key]
                                if value not in ["regex", "function"]:
                                    raise SchemaException("Entity",
                                                          "{0} - {1}- index {2}".format(entityName, entitySynonym,
                                                                                         i),
                                                          "allowed 'type' values in ['regex', 'function'] got {0}".format(
                                                              value))
                            if key == "pattern":
                                value = synonymDefinition[key]
                                if type(value) != str:
                                    raise SchemaException("Entity",
                                                          "{0} - {1}- index {2}".format(entityName, entitySynonym,
                                                                                         i),
                                                          "pattern should be a regex got {0}".format(
                                                              type(value)))
                            if key =="extractor":
                                # work more on this
                                value = synonymDefinition[key]
                                if not callable(value):
                                    raise SchemaException("Entity",
                                                          "{0} - {1}- index {2}".format(entityName, entitySynonym,
                                                                                         i),
                                                          "extractor should be a function got {0}".format(
                                                              type(value)))
                                # write extractor text here

                            if "tag" not in synonymDefinition.keys():
                                raise SchemaException("Entity",
                                                      "{0} - {1}- index {2}".format(entityName, entitySynonym, i),
                                                      "should have  a key called 'tag' ")
                            if "type" not in synonymDefinition.keys():
                                raise SchemaException("Entity",
                                                      "{0} - {1}- index {2}".format(entityName, entitySynonym, i),
                                                      "should have  a key called 'type' ")

                            if ("tag" =='regex') and "pattern" not in synonymDefinition.keys():
                                raise SchemaException("Entity",
                                                      "{0} - {1}- index {2}".format(entityName, entitySynonym, i),
                                                      "if  'tag' =='regex' you must add a key called 'pattern' with a regex value  ")

                            if ("tag" =='function') and "extractor" not in synonymDefinition.keys():
                                raise SchemaException("Entity",
                                                      "{0} - {1}- index {2}".format(entityName, entitySynonym, i),
                                                      "if  'tag' =='function' you must add a key called 'extractor' with a function that extracts the entities and a key called 'substituter' which is a function that substitues the message entities for more details refer documentation -> EntitiesHandler")

                            if ("tag" =='function') and "substituter" not in synonymDefinition.keys():
                                raise SchemaException("Entity",
                                                      "{0} - {1}- index {2}".format(entityName, entitySynonym, i),
                                                      "if  'tag' =='function' you must add a key called 'extractor' with a function that extracts the entities and a key called 'substituter' which is a function that substitues the message entities for more details refer documentation -> EntitiesHandler")
        elif schemaType =="templates":
            if type(schema) != dict:
                # check if entity is dict
                raise SchemaException("Templates", "Template samples",
                                      "Templates should be specified as a dict instead got  {0} .".format(
                                          type(schema)))
            for themeName in schema.keys():
                themeContent = schema[themeName]
                if type(themeContent) != dict:
                    raise SchemaException("Templates", themeName,
                                          "Templates should be specified as a dict instead got  {0} for theme {1}.".format(
                                              type(themeContent), themeName))
                for outputName in themeContent.keys():
                    if "_" in outputName:
                        raise SchemaException("Templates", themeName + " : " + outputName,
                                              " {0} should not contain '_' .".format(outputName))

                    outputContent = themeContent[outputName]
                    if type(outputContent) != dict:
                        raise SchemaException("Templates", themeName + " : " + outputName,
                                              "Expected format to be a dict instead got  {0} .".format(
                                                  type(outputContent)))
                    if "basic" not in outputContent.keys():
                        raise SchemaException("Templates", themeName + " : " + outputName,
                                              "Should have a 'basic' response defined i.e. key called 'basic' .")

                    for key in outputContent.keys():
                        opContent = outputContent[key]
                        if type(opContent) != list:
                            raise SchemaException("Templates", themeName + " : " + outputName + " : " + key,
                                                  "Expected type to be a list instead got {0}".format(type(opContent)))
                        for i, response in enumerate(opContent):
                            if type(response) != str:
                                raise SchemaException("Templates",
                                                      themeName + " : " + outputName + " : " + key + " index :" + str(
                                                          i),
                                                      "Expected type to be a string instead got {0}".format(
                                                          type(response)))
        elif schemaType == "testCases":
            if type(schema) != dict:
                raise SchemaException("Test Cases", "","Expected type to be a dict instead got {0}".format(type(schema)))
            else:
                for testCaseName in schema.keys():
                    testCaseContent = schema[testCaseName]
                    if "conversation" not in testCaseContent.keys():
                        raise SchemaException("TestCases", testCaseName + " : " , "Each test case must have a 'conversation'" )
                    if "description" not in testCaseContent.keys():
                        raise SchemaException("TestCases", testCaseName + " : " , "Each test case must have a 'description'"  )
                    if type(testCaseContent["description"]) != str:
                        raise SchemaException("TestCases", testCaseName + " : " , "'description' must be of type string instead got {0}".format(type(testCaseContent["description"]))  )
                    if type(testCaseContent["conversation"]) != list:
                        raise SchemaException("TestCases", testCaseName + " : " , "'conversation' should be a list of lists [[str,str],[str,str]..] instead found {0}".format(type(testCaseContent["conversation"]) ) )
                    else:
                        for i,dialog in enumerate(testCaseContent["conversation"]) :
                            if type(dialog) !=list:
                                raise SchemaException("TestCases", testCaseName + " : dialog number {0}".format(i),
                                                      "'conversation' should be a list of lists [[str,str],[str,str]..] instead found {0}".format(
                                                          type(dialog)))
                            if len(dialog) != 2:
                                raise SchemaException("TestCases", testCaseName + " : dialog number {0}".format(i),
                                                      "'conversation' should be a list of lists [[str,str],[str,str]..] each dialog should be of length 2 as multiple outputs currently not supported in test cases instead found {0}".format(dialog))
                            for conv in dialog:
                                if type(conv) != str:
                                    raise SchemaException("TestCases", testCaseName + " : dialog number {0} ".format(i),
                                                    "'conversation' should be a list of lists [[str,str],[str,str]..] instead found {0}".format(
                                                        type(conv)))
        else:
            pass



