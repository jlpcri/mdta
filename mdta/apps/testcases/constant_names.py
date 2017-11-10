# Node type name
NODE_START_NAME = ['Start', 'TestHeader Start']
NODE_TH_END_NAME = 'TestHeader End'
NODE_DATA_NAME = ['DataQueries Database', 'DataQueries WebService']
NODE_MP_NAME = ['Menu Prompt', 'Menu Prompt with Confirmation']
NODE_PLAY_PROMPT_NAME = 'Play Prompt'
NODE_SET_VARIABLE = 'Set Variable'
NODE_TRANSFER_NAME = 'Transfer'
NODE_LANGUAGE_SELECT_NAME = 'Language Select'
NODE_COMMENT_NAME = 'Comment'
NODE_DECISION_NAME = 'Decision Check'
NODE_LANGUAGE_SELECT =  'Language Select'

# Node DataQueries inputs
NODE_DATA_INPUTS = 'Inputs'
NODE_INPUTDATA_NAME = 'InputData'

# Edge type name
EDGE_DATA_NAME = 'Data'
EDGE_PRECONDITION_NAME = 'PreCondition'
EDGE_DTMF_NAME = 'DTMF'
EDGE_SPEECH_NAME = 'Speech'

# Edge Input/Output data key name
EDGE_OUTPUTDATA_NAME = 'OutputData'
EDGE_PRESS_NAME = 'Press'
EDGE_SAY_NAME = 'Say'

# Edge Invisible key name
EDGE_TYPES_INVISIBLE_KEY = 'Invisible'

# MenuPrompt property key name
ON_FAIL_GO_TO_KEY = 'OnFailGoTo'
NON_STANDARD_FAIL_KEY = 'NonStandardFail'
PLAY_BACK = 'Playback'
TTS = 'TextToSpeech'
MP_OUTPUTS = 'Outputs'
MP_DEFAULT = 'Default'
MP_NC = 'NoneConfirm'
MONOLINGUAL = 'Monolingual'
LANGUAGE = 'Language'
DEFAULT_PATH = '**'

# MenuPrompt verbiage key name
MP_VER = 'InitialPrompt'
MP_NI1 = 'NoInput1'
MP_NI2 = 'NoInput2'
MP_NM1 = 'NoMatch1'
MP_NM2 = 'NoMatch2'

# MenuPromptWithConfirmation verbiage key name
MPC_VER = 'Confirmation'
MPC_NI1 = 'ConfirmNoInput1'
MPC_NI2 = 'ConfirmNoInput2'
MPC_NM1 = 'ConfirmNoMatch1'
MPC_NM2 = 'ConfirmNoMatch2'
MPC_RJ1 = 'Reject1'
MPC_NO_VALID_INPUTS = 'MPC no valid inputs'

LANGUAGE_DEFAULT_NAME = 'English'

# Other constants
CONSTRAINTS_TRUE_OR_FALSE = 'tof'
TESTCASE_NOT_ROUTE_MESSAGE = 'This edge cannot be routed, no test case published. '

NEGATIVE_TESTS_LIST = ['NIR', 'NMR', 'NIF', 'NMF', 'NINMF']
NEGATIVE_CONFIRM_TESTS_LIST = ['CNIR', 'CNMR', 'CNIF', 'CNMF', 'CNINMF']


# TestRail tcs key name
TR_CONTENT = 'content'
TR_EXPECTED = 'expected'

# Node Positions name
NODE_POSITIONS_KEY = 'Positions'
NODE_X_KEY = 'posx'
NODE_Y_KEY = 'posy'
NODE_X_INITIAL = 100
NODE_Y_INITIAL = 100

# Node Images based on type
NODE_IMAGE = {
    NODE_START_NAME[0]: 'start',
    NODE_START_NAME[1]: 'test_header_start',
    NODE_TH_END_NAME: 'test_header_end',

    NODE_PLAY_PROMPT_NAME: 'say',
    NODE_MP_NAME[0]: 'prompt',
    NODE_MP_NAME[1]: 'prompt_with_confirm',

    NODE_DATA_NAME[0]: 'database',
    NODE_DATA_NAME[1]: 'database',
    NODE_SET_VARIABLE: 'set_variable',

    NODE_COMMENT_NAME: 'comment',
    NODE_DECISION_NAME: 'decision_check',
    NODE_TRANSFER_NAME: 'transfer',
    NODE_LANGUAGE_SELECT_NAME: 'language_select',
}