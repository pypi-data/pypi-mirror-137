from bci_framework.extensions.data_analysis import DataAnalysis, Feedback, loop_consumer, fake_loop_consumer
import logging
from bci_framework.extensions import properties as prop

from analyser import analysis
import numpy as np


########################################################################
class Analysis(DataAnalysis):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

        self.feedback = Feedback(self, 'VisualWorkingMemory')
        self.feedback.on_feedback(self.on_feedback)

        self.configuration = {}

        # Buffer
        self.create_buffer(10, aux_shape=3, fill=0)
        self.stream()

    # ----------------------------------------------------------------------
    def on_feedback(self, **feedback):
        """"""
        self.configuration = {
            'status': feedback.get('status', 'off'),
            'function': feedback.get('function', None),
            'window_analysis': feedback.get('window_analysis', None),
            'sliding_data': feedback.get('sliding_data', None),
        }

        self.set_package_size(feedback.get('sliding_data', 1000))

    # ----------------------------------------------------------------------
    @loop_consumer('eeg')
    def stream(self):
        """"""
        if not self.configuration:
            return

        if self.configuration['status'] == 'off':
            return

        window = self.buffer_eeg[:, -int(prop.SAMPLE_RATE
                                         * self.configuration['window_analysis']):]
        value = analysis(window)

        feedback = {'value': value,
                    'size': window.shape,
                    **self.configuration,
                    }
        self.feedback.write(feedback)


if __name__ == '__main__':
    Analysis(enable_produser=True)
