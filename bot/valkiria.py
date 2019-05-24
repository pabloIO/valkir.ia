from chatterbot import ChatBot
from config.config import env
class Bot(ChatBot):
    def __init__(self, nameBot, dbName):
        super().__init__(
                            nameBot,
                            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                            database_uri=env['NO_SQL_CONF']['DB_URI'],
                            database=env['NO_SQL_CONF']['DB_NAME'],
                            ## This input adapter accepts strings, dictionaries and Statements.
                            input_adapter='chatterbot.input.VariableInputTypeAdapter',
                            ## The output adapter allows the chat bot to return a response in as a Statement object.
                            output_adapter='chatterbot.output.OutputAdapter',
                            output_format='text',
                            preprocessors=[
                                'chatterbot.preprocessors.clean_whitespace'
                            ],
                            logic_adapters=[
                                {
                                    'import_path': 'chatterbot.logic.BestMatch',
                                    'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
                                    'response_selection_method': 'chatterbot.response_selection.get_most_frequent_response'
                                }
                            ],
                        )
        self.trainDataPath = 'local_data/conversacion_valkiria.csv'
        self.trainBot()
    def trainBot(self):
        from chatterbot.trainers import ListTrainer
        conversation = self.loadConversation(self.trainDataPath)
        self.set_trainer(ListTrainer)
        self.train(conversation)
    def loadConversation(self, filename):
        import csv
        conversations = []
        with open(filename, 'r') as conversation_csv:
            reader = csv.reader(conversation_csv, delimiter=",", )
            next(reader)
            for index, c in enumerate(reader):
                # print(c)
                conversations.append(c[1])
                conversations.append(c[2])
        return conversations
