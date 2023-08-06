from bci_framework.extensions.stimuli_delivery import StimuliAPI, Feedback
from bci_framework.extensions.stimuli_delivery.utils import Widgets as w
import logging

from browser import document, html, timer


########################################################################
class StimuliDelivery(StimuliAPI):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_stylesheet('styles.css')

        self.show_cross()
        self.show_synchronizer()
        
        self.feedback = Feedback(self, 'VisualWorkingMemory')
        self.feedback.on_feedback(self.on_feedback)
        
        self.bci_stimuli <= html.DIV(id='stimuli')
        
        
        self.dashboard <= w.label(
            'Visual working memory - Neurofeedback', 'headline4')
        self.dashboard <= html.BR()
        
        self.dashboard <= w.subject_information(paradigm='Visual working memory - Neurofeedback')
        
        self.dashboard <= w.slider(
            label='Baseline acquisition:',
            min=1,
            max=5,
            value=1,
            step=0.1,
            unit='m',
            id='baseline_duration',
            # on_change=self.configure_analyser,
        )
        self.dashboard <= w.slider(
            label='Sesion duration:',
            min=5,
            max=30,
            value=10,
            step=0.1,
            unit='m',
            id='sesion_duration',
            # on_change=self.configure_analyser,
        )
        
        self.dashboard <= w.slider(
            label='Window analysis:',
            min=0.5,
            max=2,
            value=1,
            step=0.1,
            unit='s',
            id='window_analysis',
            # on_change=self.configure_analyser,
        )
        
        self.dashboard <= w.slider(
            label='Sliding data:',
            min=100,
            max=2000,
            value=1000,
            step=100,
            id='sliding_data',
            # on_change=self.configure_analyser,
        )
        
        self.dashboard <= w.select(
            'Analysis Function', 
            [['fn1', 'fn1'], ['fn2', 'fn2'], ['fn3', 'fn3']], 
            value='fn1',
            id='analysis_function',
            # on_change=self.configure_analyser,
        )
        
        
        self.dashboard <= w.toggle_button([('Start session', self.start), ('Stop session', self.stop)], id='run')



    # ----------------------------------------------------------------------
    def on_feedback(self, **feedback):
        """"""
        value = feedback['value']
        value_p = self.map(value, -1, 1, 0, 100)
        document.select_one('#stimuli').style = {'background-position-x': f'{value_p}%'}
        

    # ----------------------------------------------------------------------
    def start(self) -> None:
        """Start the run.

        A run consist in a consecutive pipeline trials execution.
        """
        if w.get_value('record'):
            self.start_record()

        self.build_trials()
        
        self.show_counter(5)
        timer.set_timeout(self.start_run, 5000)
        
    # ----------------------------------------------------------------------
    def start_run(self):
        """"""
        self.run_pipeline(self.pipeline_trial, self.trials, callback='stop_run')

    # ----------------------------------------------------------------------
    def stop(self) -> None:
        """Stop pipeline execution."""
        self.stop_pipeline()

    # ----------------------------------------------------------------------
    def stop_run(self) -> None:
        """Stop pipeline execution."""
        document.select_one('#stimuli').style = {'display': 'none'}
        w.get_value('run').off()
        if w.get_value('record'):
            timer.set_timeout(self.stop_record, 2000)

    # ----------------------------------------------------------------------
    def build_trials(self) -> None:
        """Define the `trials` and `pipeline trials`.

        The `trials` consist (in this case) in a list of cues.
        The `pipeline trials` is a set of couples `(callable, duration)` that
        define a single trial, this list of functions are executed asynchronously
        and repeated for each trial.
        """
    
        baseline_duration = w.get_value('baseline_duration') * 60 * 1000
        sesion_duration = w.get_value('sesion_duration') * 60 * 1000
        
        self.trials = [{
            'function': w.get_value('analysis_function'),
            # 'baseline_duration': w.get_value('baseline_duration'),
            'window_analysis': w.get_value('window_analysis'),
            'sliding_data': w.get_value('sliding_data'),
        }]
        
        self.pipeline_trial = [
            ['configure_analyser', 1000], 
            # ['baseline', baseline_duration],  
            # ['session', sesion_duration],
            ['baseline', 2000],  
            ['session', 7000],
            ['stop_analyser', 1000],
        ]
    
    # ----------------------------------------------------------------------
    def baseline(self, *args, **kwargs):
        """"""
        self.show_cross()
        document.select_one('#stimuli').style = {'display': 'none'}


    # ----------------------------------------------------------------------
    def session(self, *args, **kwargs):
        """"""
        document.select_one('#stimuli').style = {'display': 'block'}


    # ----------------------------------------------------------------------
    def configure_analyser(self, function, window_analysis, sliding_data):
        """"""
        self.feedback.write({
            'status': 'on',
            'function': function,
            'window_analysis': window_analysis,
            'sliding_data': sliding_data,
        })
        
    # ----------------------------------------------------------------------
    def stop_analyser(self):
        """"""
        self.feedback.write({
            'status': 'off',
        })
            

            
if __name__ == '__main__':
    StimuliDelivery()


