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
        self.trainBot()
    def trainBot(self):
        from chatterbot.trainers import ListTrainer
        self.set_trainer(ListTrainer)
        self.train([
            'Hola ¿como estas?',
            'Hola, estoy bien, ¿y tu?',
            'Pues ando con problemas', 
            '¿Por que?',
            'He reprobado una materia en la Universidad',
            'Que mal, pero no te desanimes, hay muchas mas oportunidades',
            'Muchas gracias'
        ])