from config.config import env

class Chatter(object):
    @staticmethod
    def answer(bot, msg, conversation_id):
        try:
            # conv = bot.create_conversation()
            # print(conv)
            response =  bot.get_response(msg, conversation_id).serialize()['text']
            return response
            # num_words = response.split(' ')
            # emit('is_writing', {'time': num_words * env['CHILD_TIME_WRITING_FACTOR']})
            # time()
        except Exception as e:
            print(e)
