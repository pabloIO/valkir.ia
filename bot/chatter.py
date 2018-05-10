from config.config import env

class Chatter(object):
    @staticmethod
    def answer(bot, msg):
        try:
            # conv = bot.create_conversation()
            # print(conv)
            response =  bot.get_response(msg).serialize()['text']
            num_words = response.split(' ')
            # emit('is_writing', {'time': num_words * env['CHILD_TIME_WRITING_FACTOR']})
            # time()
        except Exception as e:
            print(e)
