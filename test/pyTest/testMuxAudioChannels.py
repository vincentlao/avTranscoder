import os

 # Check if environment is setup to run the tests
if os.environ.get('AVTRANSCODER_TEST_AUDIO_WAVE_FILE') is None or \
    os.environ.get('AVTRANSCODER_TEST_AUDIO_MOV_FILE') is None:
    from nose.plugins.skip import SkipTest
    raise SkipTest("Need to define environment variables "
        "AVTRANSCODER_TEST_AUDIO_WAVE_FILE and "
        "AVTRANSCODER_TEST_AUDIO_MOV_FILE")

from nose.tools import *

from pyAvTranscoder import avtranscoder as av

def testMuxAudioChannelsFromDifferentFormatInputs_20():
    """
    Mux audio channels from different formats files, and generate one audio stereo stream
    """
    # inputs
    inputFileName1 = os.environ['AVTRANSCODER_TEST_AUDIO_MOV_FILE']
    inputFileName2 = os.environ['AVTRANSCODER_TEST_AUDIO_WAVE_FILE']
    assert_not_equals(inputFileName1, inputFileName2)

    inputs = av.InputStreamDescVector()
    inputs.append(av.InputStreamDesc(inputFileName1, 1, 1))
    inputs.append(av.InputStreamDesc(inputFileName2, 0, 2))

    # output
    outputFileName = "testMuxAudioChannelsFromDifferentFormatInputs_20.wav"
    ouputFile = av.OutputFile(outputFileName)

    transcoder = av.Transcoder(ouputFile)
    transcoder.addStream(inputs, "wave24b48kstereo")

    progress = av.ConsoleProgress()
    processStat = transcoder.process( progress )

    # check process stat returned
    audioStat = processStat.getAudioStat(0)

    inputFile1 = av.InputFile(inputFileName1)
    inputFile2 = av.InputFile(inputFileName2)

    src_audioStream1 = inputFile1.getProperties().getAudioProperties()[0]
    src_audioStream2 = inputFile2.getProperties().getAudioProperties()[0]

    min_src_duration = min(src_audioStream1.getDuration(), src_audioStream2.getDuration())

    assert_equals(min_src_duration, audioStat.getDuration())

    # check dst file properties
    dst_inputFile = av.InputFile(outputFileName)
    dst_fileProperties = dst_inputFile.getProperties()
    assert_equals(min_src_duration, dst_fileProperties.getDuration())

    # check dst audio streams
    dst_audioProperties = dst_fileProperties.getAudioProperties()
    assert_equals(1, len(dst_audioProperties))
    assert_equals(2, dst_audioProperties[0].getNbChannels())

def testMuxAudioChannelsFromDifferentFormatInputs_51():
    """
    Mux audio channels from different formats files, and generate one audio 5.1 stream
    """
    # inputs
    inputFileName1 = os.environ['AVTRANSCODER_TEST_AUDIO_MOV_FILE']
    inputFileName2 = os.environ['AVTRANSCODER_TEST_AUDIO_WAVE_FILE']
    assert_not_equals(inputFileName1, inputFileName2)

    inputs = av.InputStreamDescVector()
    inputs.append(av.InputStreamDesc(inputFileName1, 1, 1))
    inputs.append(av.InputStreamDesc(inputFileName1, 1, 0))
    inputs.append(av.InputStreamDesc(inputFileName2, 0, 2))
    inputs.append(av.InputStreamDesc(inputFileName2, 0, 5))
    inputs.append(av.InputStreamDesc(inputFileName2, 0, 1))
    inputs.append(av.InputStreamDesc(inputFileName2, 0, 3))

    # output
    outputFileName = "testMuxAudioChannelsFromDifferentFormatInputs_51.wav"
    ouputFile = av.OutputFile(outputFileName)

    transcoder = av.Transcoder(ouputFile)
    transcoder.addStream(inputs, "wave24b48k5_1")

    progress = av.ConsoleProgress()
    processStat = transcoder.process( progress )

    # check process stat returned
    audioStat = processStat.getAudioStat(0)

    inputFile1 = av.InputFile(inputFileName1)
    inputFile2 = av.InputFile(inputFileName2)

    src_audioStream1 = inputFile1.getProperties().getAudioProperties()[0]
    src_audioStream2 = inputFile2.getProperties().getAudioProperties()[0]

    min_src_duration = min(src_audioStream1.getDuration(), src_audioStream2.getDuration())

    assert_equals(min_src_duration, audioStat.getDuration())

    # check dst file properties
    dst_inputFile = av.InputFile(outputFileName)
    dst_fileProperties = dst_inputFile.getProperties()
    assert_equals(min_src_duration, dst_fileProperties.getDuration())

    # check dst audio streams
    dst_audioProperties = dst_inputFile.getProperties().getAudioProperties()
    assert_equals(1, len(dst_audioProperties))
    assert_equals(6, dst_audioProperties[0].getNbChannels())


def testMuxAudioChannelsWithSilence_20():
    """
    Mux audio channels with generated silence, and generate one audio stereo stream
    """
    # input
    inputFileName = os.environ['AVTRANSCODER_TEST_AUDIO_WAVE_FILE']

    inputs = av.InputStreamDescVector()
    inputs.append(av.InputStreamDesc(inputFileName, 0, 0))
    inputs.append(av.InputStreamDesc("", 0, 0)) # empty filename to generate silence

    # output
    outputFileName = "testMuxAudioChannelsWithSilence_20.wav"
    ouputFile = av.OutputFile(outputFileName)

    transcoder = av.Transcoder(ouputFile)
    transcoder.addStream(inputs, "wave24b48kstereo")

    progress = av.ConsoleProgress()
    processStat = transcoder.process( progress )

    # check process stat returned
    audioStat = processStat.getAudioStat(0)

    inputFile = av.InputFile(inputFileName)

    src_audioStream = inputFile.getProperties().getAudioProperties()[0]

    assert_equals(src_audioStream.getDuration(), audioStat.getDuration())

    # check dst file properties
    dst_inputFile = av.InputFile(outputFileName)
    dst_fileProperties = dst_inputFile.getProperties()
    assert_equals(src_audioStream.getDuration(), dst_fileProperties.getDuration())

    # check dst audio streams
    dst_audioProperties = dst_fileProperties.getAudioProperties()
    assert_equals(1, len(dst_audioProperties))
    assert_equals(2, dst_audioProperties[0].getNbChannels())

def testMuxAudioChannelsWithSilenceProfileFromInput_20():
    """
    Mux audio channels with generated silence, and generate one audio stereo stream
    """
    # input
    inputFileName = os.environ['AVTRANSCODER_TEST_AUDIO_WAVE_FILE']

    inputs = av.InputStreamDescVector()
    inputs.append(av.InputStreamDesc(inputFileName, 0, 0))
    inputs.append(av.InputStreamDesc("", 0, 0)) # empty filename to generate silence

    # output
    outputFileName = "testMuxAudioChannelsWithSilenceNoProfile_20.wav"
    ouputFile = av.OutputFile(outputFileName)

    transcoder = av.Transcoder(ouputFile)
    transcoder.addStream(inputs)

    progress = av.ConsoleProgress()
    processStat = transcoder.process( progress )

    # check process stat returned
    audioStat = processStat.getAudioStat(0)

    inputFile = av.InputFile(inputFileName)

    src_audioStream = inputFile.getProperties().getAudioProperties()[0]

    assert_equals(src_audioStream.getDuration(), audioStat.getDuration())

    # check dst file properties
    dst_inputFile = av.InputFile(outputFileName)
    dst_fileProperties = dst_inputFile.getProperties()
    assert_equals(src_audioStream.getDuration(), dst_fileProperties.getDuration())

    # check dst audio streams
    dst_audioProperties = dst_fileProperties.getAudioProperties()
    assert_equals(1, len(dst_audioProperties))
    assert_equals(2, dst_audioProperties[0].getNbChannels())

def testMuxAudioChannelsWithSilenceProfileFromInput_51():
    """
    Mux audio channels with generated silence, and generate one audio 5.1 stream
    """
    # inputs
    inputFileName1 = os.environ['AVTRANSCODER_TEST_AUDIO_MOV_FILE']
    inputFileName2 = os.environ['AVTRANSCODER_TEST_AUDIO_WAVE_FILE']
    assert_not_equals(inputFileName1, inputFileName2)

    inputs = av.InputStreamDescVector()
    inputs.append(av.InputStreamDesc("", 0, 0)) # empty filename to generate silence
    inputs.append(av.InputStreamDesc(inputFileName1, 1, 0))
    inputs.append(av.InputStreamDesc(inputFileName2, 0, 2))
    inputs.append(av.InputStreamDesc("", 0, 0)) # empty filename to generate silence
    inputs.append(av.InputStreamDesc(inputFileName2, 0, 1))
    inputs.append(av.InputStreamDesc("", 0, 0)) # empty filename to generate silence

    # output
    outputFileName = "testMuxAudioChannelsWithSilenceProfileFromInput_51.wav"
    ouputFile = av.OutputFile(outputFileName)

    transcoder = av.Transcoder(ouputFile)
    transcoder.addStream(inputs)

    progress = av.ConsoleProgress()
    processStat = transcoder.process( progress )

    # check process stat returned
    audioStat = processStat.getAudioStat(0)

    inputFile1 = av.InputFile(inputFileName1)
    inputFile2 = av.InputFile(inputFileName2)

    src_audioStream1 = inputFile1.getProperties().getAudioProperties()[0]
    src_audioStream2 = inputFile2.getProperties().getAudioProperties()[0]

    min_src_duration = min(src_audioStream1.getDuration(), src_audioStream2.getDuration())

    assert_equals(min_src_duration, audioStat.getDuration())

    # check dst file properties
    dst_inputFile = av.InputFile(outputFileName)
    dst_fileProperties = dst_inputFile.getProperties()
    assert_equals(min_src_duration, dst_fileProperties.getDuration())

    # check dst audio streams
    dst_audioProperties = dst_inputFile.getProperties().getAudioProperties()
    assert_equals(1, len(dst_audioProperties))
    assert_equals(6, dst_audioProperties[0].getNbChannels())

@raises(RuntimeError)
def testMuxAudioChannelsWithSilenceOnly_20():
    """
    Mux audio channels with generated silence, and generate one audio stereo stream
    """
    # input
    inputs = av.InputStreamDescVector()
    inputs.append(av.InputStreamDesc("", 0, 0)) # empty filename to generate silence
    inputs.append(av.InputStreamDesc("", 0, 0)) # empty filename to generate silence

    # output
    outputFileName = "testMuxAudioChannelsWithSilenceOnly_20.wav"
    ouputFile = av.OutputFile(outputFileName)

    transcoder = av.Transcoder(ouputFile)
    transcoder.addStream(inputs, "wave24b48kstereo")

    progress = av.ConsoleProgress()
    processStat = transcoder.process( progress )

