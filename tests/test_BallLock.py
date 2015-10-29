import unittest

from mpf.system.machine import MachineController
from MpfTestCase import MpfTestCase
from mock import MagicMock
import time

class TestBallLock(MpfTestCase):

    def getConfigFile(self):
        return 'test_ball_lock.yaml'

    def getMachinePath(self):
        return '../tests/machine_files/ball_device/'

    def _missing_ball(self):
        self._missing += 1

    def _requesting_ball(self, balls, **kwargs):
        self._requesting += balls

    def _ball_enter(self, balls, **kwargs):
        self._enter += balls

    def _captured_from_pf(self, balls, **kwargs):
        self._captured += balls

    def _captured_from_pf(self, balls, **kwargs):
        self._captured += balls

    def _collecting_balls_complete_handler(self, **kwargs):
        self._collecting_balls_complete = 1

    def test_lock_and_release_at_game_end(self):
        coil1 = self.machine.coils['eject_coil1']
        coil2 = self.machine.coils['eject_coil2']
        coil3 = self.machine.coils['eject_coil3']
        trough = self.machine.ball_devices['test_trough']
        launcher = self.machine.ball_devices['test_launcher']
        lock = self.machine.ball_devices['test_lock']
        lock_logic = self.machine.ball_locks['lock_test']
        playfield = self.machine.ball_devices['playfield']

        self.machine.events.add_handler('balldevice_captured_from_playfield', self._captured_from_pf)
        self.machine.events.add_handler('balldevice_1_ball_missing', self._missing_ball)
        self.machine.events.add_handler('balldevice_test_launcher_ball_request', self._requesting_ball)
        self.machine.events.add_handler('collecting_balls_complete', self._collecting_balls_complete_handler)


        self._enter = 0
        self._captured = 0
        self._missing = 0
        self._requesting = 0
        self._collecting_balls_complete = 0
        self.machine.ball_controller.num_balls_known = 2

        # add an initial ball to trough
        self.machine.switch_controller.process_switch("s_ball_switch1", 1)
        self.machine.switch_controller.process_switch("s_ball_switch2", 1)
        self.advance_time_and_run(1)
        self.assertEquals(2, self._captured)
        self._captured = 0
        self.assertEquals(0, playfield.balls)
        self.assertEquals(2, self.machine.ball_controller.num_balls_known)

        # it should keep the ball
        coil1.pulse = MagicMock()
        coil2.pulse = MagicMock()
        coil3.pulse = MagicMock()
        self.assertEquals(2, trough.count_balls())
        assert not coil1.pulse.called
        assert not coil2.pulse.called
        assert not coil3.pulse.called

        # start a game
        self.machine.switch_controller.process_switch("s_start", 1)
        self.advance_time_and_run(0.1)
        self.machine.switch_controller.process_switch("s_start", 0)
        self.advance_time_and_run(1)
        self.assertEquals(1, self._requesting)
        self._requesting = 0

        # trough ejects
        coil1.pulse.assert_called_once_with()
        assert not coil2.pulse.called
        assert not coil3.pulse.called

        self.machine.switch_controller.process_switch("s_ball_switch1", 0)
        self.advance_time_and_run(1)
        self.assertEquals(1, trough.count_balls())


        # launcher receives and ejects
        self.machine.switch_controller.process_switch("s_ball_switch_launcher", 1)
        self.advance_time_and_run(1)
        self.assertEquals(1, launcher.count_balls())

        coil1.pulse.assert_called_once_with()
        coil2.pulse.assert_called_once_with()
        assert not coil3.pulse.called

        # launcher shoots the ball
        self.machine.switch_controller.process_switch("s_ball_switch_launcher", 0)
        self.advance_time_and_run(1)
        self.assertEquals(0, launcher.count_balls())

        self.machine.switch_controller.process_switch("s_playfield_active", 1)
        self.advance_time_and_run(0.1)
        self.machine.switch_controller.process_switch("s_playfield_active", 0)
        self.advance_time_and_run(1)

        self.assertEquals(1, playfield.balls)
        self.assertEquals(0, self._captured)
        self.assertEquals(0, self._missing)

        coil1.pulse = MagicMock()
        coil2.pulse = MagicMock()
        coil3.pulse = MagicMock()

        # ball enters lock 
        self.machine.switch_controller.process_switch("s_ball_switch_lock1", 1)
        self.advance_time_and_run(1)
        self.assertEquals(1, lock.count_balls())

        # it will request another ball
        coil1.pulse.assert_called_once_with()
        assert not coil2.pulse.called
        assert not coil3.pulse.called

        self.assertEquals(0, playfield.balls)
        self.assertEquals(1, self._captured)
        self.assertEquals(0, self._missing)
        self.assertEquals(1, lock_logic.balls_locked)
        self._captured = 0
        self.assertEquals(1, self._requesting)
        self._requesting = 0

        self.machine.switch_controller.process_switch("s_ball_switch2", 0)
        self.advance_time_and_run(1)
        self.assertEquals(0, trough.count_balls())


        # launcher receives and ejects
        self.machine.switch_controller.process_switch("s_ball_switch_launcher", 1)
        self.advance_time_and_run(1)
        self.assertEquals(1, launcher.count_balls())

        coil1.pulse.assert_called_once_with()
        coil2.pulse.assert_called_once_with()
        assert not coil3.pulse.called

        # launcher shoots the ball
        self.machine.switch_controller.process_switch("s_ball_switch_launcher", 0)
        self.advance_time_and_run(1)
        self.assertEquals(0, launcher.count_balls())

        self.machine.switch_controller.process_switch("s_playfield_active", 1)
        self.advance_time_and_run(0.1)
        self.machine.switch_controller.process_switch("s_playfield_active", 0)
        self.advance_time_and_run(1)

        self.assertEquals(1, playfield.balls)
        self.assertEquals(0, self._captured)
        self.assertEquals(0, self._missing)

        # ball drains and game ends
        self.machine.switch_controller.process_switch("s_ball_switch1", 1)
        self.advance_time_and_run(1)

        self.assertEquals(0, playfield.balls)
        self.assertEquals(1, self._captured)
        self.assertEquals(0, self._missing)
        self._captured = 0
        self.assertEquals(2, self.machine.ball_controller.num_balls_known)

        # lock should eject all balls
        coil1.pulse.assert_called_once_with()
        coil2.pulse.assert_called_once_with()
        coil3.pulse.assert_called_once_with()

        self.machine.switch_controller.process_switch("s_ball_switch_lock1", 0)
        self.advance_time_and_run(1)
        self.assertEquals(0, lock.count_balls())
        self.assertEquals(0, lock_logic.balls_locked)
        self.assertEquals(0, self._captured)
        self.assertEquals(0, self._missing)

        self.assertEquals(0, self._collecting_balls_complete)

        # ball also drains
        self.machine.switch_controller.process_switch("s_ball_switch2", 1)
        self.advance_time_and_run(1)
        self.assertEquals(0, playfield.balls)
        self.assertEquals(1, self._captured)
        self.assertEquals(0, self._missing)
        self.assertEquals(0, self._requesting)

        self.assertEquals(2, self.machine.ball_controller.num_balls_known)
        self.assertEquals(1, self._collecting_balls_complete)

        self.advance_time_and_run(100)
        self.assertEquals(0, playfield.balls)
        self.assertEquals(1, self._captured)
        self.assertEquals(0, self._missing)
        self.assertEquals(0, self._requesting)

        self.assertEquals(2, self.machine.ball_controller.num_balls_known)
        self.assertEquals(1, self._collecting_balls_complete)

