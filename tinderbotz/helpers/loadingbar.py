import sys
import time

class LoadingBar:

    def __init__(self, length_of_loop, explanation="", amount_of_bars=30):

        self.length_of_loop = length_of_loop
        self.explanation = explanation
        self.amount_of_bars = amount_of_bars
        self.update_loading(index=-1)

    def update_loading(self, index):
        sys.stdout.write('\r')

        # To avoid dividing by Zero, let's do a check
        if self.length_of_loop == 0:
            percentage_loaded = 100
        else:
            percentage_loaded = int((index + 1)*100 / self.length_of_loop)

        if percentage_loaded > 100:
            percentage_loaded = 100

        # [===>----] 45% of new matches scraped
        amount_of_equals = int(percentage_loaded / 100 * self.amount_of_bars)
        amount_of_minus = self.amount_of_bars - amount_of_equals - 1

        printout = "[{}>{}] {}% of the {} handled.".format('=' * amount_of_equals, '-' * amount_of_minus, percentage_loaded,
                                            self.explanation)
        sys.stdout.write(printout)
        sys.stdout.flush()
        time.sleep(0.25)

        if percentage_loaded == 100:
            print("\n")
