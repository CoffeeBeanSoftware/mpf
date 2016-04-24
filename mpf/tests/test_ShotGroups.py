from mock import MagicMock

from mpf.core.rgb_color import RGBColor
from mpf.tests.MpfTestCase import MpfTestCase


class TestShotGroups(MpfTestCase):

    def getConfigFile(self):
        return 'test_shot_groups.yaml'

    def getMachinePath(self):
        return 'tests/machine_files/shots/'

    def start_game(self):
        # shots only work in games so we have to do this a lot
        self.machine.playfield.add_ball = MagicMock()
        self.machine.events.post('game_start')
        self.advance_time_and_run()
        self.machine.game.balls_in_play = 1
        self.assertIsNotNone(self.machine.game)

    def stop_game(self):
        # stop game
        self.machine.game.game_ending()
        self.advance_time_and_run()
        self.assertIsNone(self.machine.game)

    def test_disabled_when_no_game(self):
        # all shot group functionality should be disabled if there is not a
        # game in progress. Really we're just making sure this doesn't crash.

        self.machine.events.post('s_rotate_l_active')
        self.advance_time()

        self.hit_and_release_switch("switch_1")
        self.hit_and_release_switch("switch_2")
        self.hit_and_release_switch("switch_3")
        self.hit_and_release_switch("switch_4")

    def test_events_and_complete(self):
        self.start_game()

        self.mock_event("test_group_default_lit_complete")
        self.mock_event("test_group_default_unlit_complete")
        self.mock_event("test_group_default_lit_hit")
        self.mock_event("test_group_default_unlit_hit")
        self.mock_event("test_group_default_hit")
        self.mock_event("test_group_hit")

        self.hit_and_release_switch("switch_1")

        # it should post events. here for the previous(?) profile state
        self.assertEqual(0, self._events['test_group_default_lit_hit'])
        self.assertEqual(1, self._events['test_group_default_unlit_hit'])
        self.assertEqual(1, self._events['test_group_default_hit'])
        self.assertEqual(1, self._events['test_group_hit'])

        self.hit_and_release_switch("switch_1")

        # it posts the opposite state
        self.assertEqual(0, self._events['test_group_default_lit_complete'])
        self.assertEqual(0, self._events['test_group_default_unlit_complete'])
        self.assertEqual(1, self._events['test_group_default_lit_hit'])
        self.assertEqual(1, self._events['test_group_default_unlit_hit'])
        self.assertEqual(2, self._events['test_group_default_hit'])
        self.assertEqual(2, self._events['test_group_hit'])

        self.hit_and_release_switch("switch_2")
        self.hit_and_release_switch("switch_3")
        self.hit_and_release_switch("switch_4")

        self.assertEqual(1, self._events['test_group_default_lit_complete'])
        self.assertEqual(0, self._events['test_group_default_unlit_complete'])
        self.assertEqual(1, self._events['test_group_default_lit_hit'])
        self.assertEqual(4, self._events['test_group_default_unlit_hit'])
        self.assertEqual(5, self._events['test_group_default_hit'])
        self.assertEqual(5, self._events['test_group_hit'])

        self.stop_game()

    def test_rotate(self):
        self.start_game()

        self.mock_event("test_group_default_lit_complete")

        self.assertEqual("unlit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("switch_1")

        self.assertEqual("lit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_r")

        self.assertEqual("unlit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("switch_1")

        self.assertEqual("lit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_r")

        self.assertEqual("unlit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_r")

        self.assertEqual("unlit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_r")

        self.assertEqual("lit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_l")

        self.assertEqual("unlit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("lit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

    def test_shot_group_in_mode(self):
        self.start_game()

        self.hit_and_release_switch("switch_1")

        self.assertEqual("lit", self.machine.shots.shot_1.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_2.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_3.get_profile_by_key('mode', None)[
            'current_state_name'])
        self.assertEqual("unlit", self.machine.shots.shot_4.get_profile_by_key('mode', None)[
            'current_state_name'])

        # Start the mode
        self.machine.modes.mode_shot_groups.start()
        self.advance_time_and_run()

        self.assertEqual("one", self.machine.shots.shot_1.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_2.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_3.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("unlit",
                         self.machine.shots.shot_4.get_profile_by_key(
                             'mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("switch_1")
        self.assertEqual("two", self.machine.shots.shot_1.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_2.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_3.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("unlit",
                         self.machine.shots.shot_4.get_profile_by_key(
                             'mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_l")
        self.assertEqual("one", self.machine.shots.shot_1.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_2.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("two", self.machine.shots.shot_3.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("lit",
                         self.machine.shots.shot_4.get_profile_by_key(
                             'mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_l")
        self.assertEqual("one", self.machine.shots.shot_1.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("two", self.machine.shots.shot_2.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_3.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("unlit",
                         self.machine.shots.shot_4.get_profile_by_key(
                             'mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_l")
        self.assertEqual("two", self.machine.shots.shot_1.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_2.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_3.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("unlit",
                         self.machine.shots.shot_4.get_profile_by_key(
                             'mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_l")
        self.assertEqual("one", self.machine.shots.shot_1.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_2.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("two", self.machine.shots.shot_3.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("unlit",
                         self.machine.shots.shot_4.get_profile_by_key(
                             'mode', None)[
            'current_state_name'])

        self.hit_and_release_switch("s_rotate_r")
        self.assertEqual("two", self.machine.shots.shot_1.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_2.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("one", self.machine.shots.shot_3.get_profile_by_key('mode', self.machine.modes.mode_shot_groups)[
            'current_state_name'])
        self.assertEqual("unlit",
                         self.machine.shots.shot_4.get_profile_by_key(
                             'mode', None)[
            'current_state_name'])

    def test_rotate_with_shows_in_progress(self):
        # also tests profile from shot_group with no profile in shots
        self.start_game()
        self.advance_time_and_run()

        # advance the shots a bit

        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_10.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_11.hw_driver.current_color)

        self.hit_and_release_switch('switch_10')
        self.advance_time_and_run()
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_10.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_11.hw_driver.current_color)

        self.hit_and_release_switch('switch_10')
        self.advance_time_and_run()
        self.assertEqual(RGBColor('orange'),
            self.machine.leds.led_10.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_11.hw_driver.current_color)

        self.hit_and_release_switch('switch_11')
        self.advance_time_and_run()
        self.assertEqual(RGBColor('orange'),
            self.machine.leds.led_10.hw_driver.current_color)
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_11.hw_driver.current_color)

        # rotate
        self.machine.events.post('rotate_11_left')
        self.advance_time_and_run()
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_10.hw_driver.current_color)
        self.assertEqual(RGBColor('orange'),
            self.machine.leds.led_11.hw_driver.current_color)

        # make sure they don't auto advance since the shows should be set to
        # manual advance
        self.advance_time_and_run()
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_10.hw_driver.current_color)
        self.assertEqual(RGBColor('orange'),
            self.machine.leds.led_11.hw_driver.current_color)

        self.advance_time_and_run()
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_10.hw_driver.current_color)
        self.assertEqual(RGBColor('orange'),
            self.machine.leds.led_11.hw_driver.current_color)

    def test_no_profile_in_shot_group_uses_profile_from_shot(self):
        self.start_game()
        self.advance_time_and_run()

        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_30.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_31.hw_driver.current_color)

        self.hit_and_release_switch('switch_30')
        self.advance_time_and_run()
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_30.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_31.hw_driver.current_color)

        self.hit_and_release_switch('switch_30')
        self.advance_time_and_run()
        self.assertEqual(RGBColor('orange'),
            self.machine.leds.led_30.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_31.hw_driver.current_color)

        self.hit_and_release_switch('switch_31')
        self.advance_time_and_run()
        self.assertEqual(RGBColor('orange'),
            self.machine.leds.led_30.hw_driver.current_color)
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_31.hw_driver.current_color)

    def test_control_events(self):
        # tests control events at the shot_group level

        shot32 = self.machine.shots.shot_32
        shot33 = self.machine.shots.shot_33
        group32 = self.machine.shot_groups.shot_group_32

        self.mock_event("shot_32_hit")
        self.mock_event("shot_33_hit")
        self.mock_event("shot_group_32_hit")

        self.start_game()

        # Since this shot has custom enable events, it should not be enabled on
        # game start
        self.assertFalse(shot32.enabled)
        self.assertFalse(shot33.enabled)
        self.assertFalse(group32.enabled)

        # test enabling via event
        self.machine.events.post('group32_enable')
        self.advance_time_and_run()

        self.assertTrue(shot32.enabled)
        self.assertTrue(shot33.enabled)
        self.assertTrue(group32.enabled)

        # test advance event
        self.assertEqual(shot32.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_32.hw_driver.current_color)
        self.assertEqual(shot33.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_33.hw_driver.current_color)

        self.machine.events.post('group32_advance')
        self.advance_time_and_run()
        self.assertEqual(shot32.profiles[0]['current_state_name'], 'red')
        self.assertEqual(shot33.profiles[0]['current_state_name'], 'red')
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_32.hw_driver.current_color)
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_33.hw_driver.current_color)

        # test reset event
        self.machine.events.post('group32_reset')
        self.advance_time_and_run()
        self.assertEqual(shot32.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(shot33.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_32.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_33.hw_driver.current_color)

        # test rotate without rotation enabled
        shot32.advance()
        self.advance_time_and_run()
        self.assertEqual(shot32.profiles[0]['current_state_name'], 'red')
        self.assertEqual(shot33.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_32.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_33.hw_driver.current_color)
        self.assertFalse(group32.rotation_enabled)

        self.machine.events.post('group32_rotate')
        self.advance_time_and_run()
        self.assertEqual(shot32.profiles[0]['current_state_name'], 'red')
        self.assertEqual(shot33.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_32.hw_driver.current_color)
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_33.hw_driver.current_color)

        # test rotation enable
        self.machine.events.post('group32_enable_rotation')
        self.advance_time_and_run()
        self.assertTrue(group32.rotation_enabled)

        # test that rotate works now
        self.machine.events.post('group32_rotate')
        self.advance_time_and_run()
        self.assertEqual(shot32.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(shot33.profiles[0]['current_state_name'], 'red')
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_32.hw_driver.current_color)
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_33.hw_driver.current_color)

        # test disable rotation
        self.machine.events.post('group32_disable_rotation')
        self.advance_time_and_run()
        self.assertFalse(group32.rotation_enabled)

        # test that rotate works now
        self.machine.events.post('group32_rotate')
        self.advance_time_and_run()

        # test that rotate did not happen
        self.assertEqual(shot32.profiles[0]['current_state_name'], 'unlit')
        self.assertEqual(shot33.profiles[0]['current_state_name'], 'red')
        self.assertEqual(RGBColor('off'),
            self.machine.leds.led_32.hw_driver.current_color)
        self.assertEqual(RGBColor('red'),
            self.machine.leds.led_33.hw_driver.current_color)

        # test disable event
        self.machine.events.post('group32_disable')
        self.advance_time_and_run()
        self.assertFalse(shot32.enabled)
        self.assertFalse(shot33.enabled)
        self.assertFalse(group32.enabled)

    def test_control_events_in_mode(self):
        pass  # todo

    def test_state_names_to_rotate(self):
        pass

    def test_state_names_to_not_rotate(self):
        pass

    def test_rotation_pattern(self):
        pass

    def test_adding_and_removing_from_group(self):
        pass
