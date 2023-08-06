import os
import shutil
import base64
import logging
from boldqc.bids import BIDS
import boldqc.tasks as tasks
from executors.models import Job

logger = logging.getLogger(__file__)

class Task(tasks.BaseTask):
    def __init__(self, infile, outdir, tempdir=None, pipenv=None):
        self._infile = infile
        super().__init__(outdir, tempdir, pipenv)

    def build(self):
        cmd = [
            'selfie',
            '--lock',
            '--output-file', self._prov,
            'niftiqa_wrapper.py',
            '--skip', '4',
            '--mask-threshold', '150.0',
            '--output-dir', self._outdir
        ]
        cmd.append(self._infile)
        logger.debug(cmd)
        if self._pipenv:
            os.chdir(self._pipenv)
            cmd[:0] = ['pipenv', 'run']
        logdir = self.logdir()
        # copy json sidecar into output logs directory
        sidecar = BIDS.sidecar_for_image(self._infile)
        destination = os.path.join(logdir, os.path.basename(sidecar))
        logger.debug('copying %s to %s', sidecar, destination)
        shutil.copy2(sidecar, destination)
        # return job object
        log = os.path.join(logdir, 'niftiqa_wrapper.log')
        self.job = Job(
            name='niftiqa',
            time='1440',
            memory='3G',
            command=cmd,
            output=log,
            error=log
        )

