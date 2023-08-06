# Copyright Exafunction, Inc.

import exa._C as _C
import exa.ffmpeg_pb.ffmpeg_pb2 as ffmpeg_pb2
from exa.py_client import Session
from exa.py_value import Value


class VideoDecoder:
    """
    VideoDecoder represents a remote video decoder.

    To use VideoDecoder, FfmpegDecode must be included in the placement group.
    """

    def __init__(
        self,
        sess: Session,
        filename: str,
        dec_params: ffmpeg_pb2.DecoderParameters,
    ):
        """
        Create a VideoDecoder from a video file.

        :param sess: The Exafunction session to use
        :param filename: The path to the video file
        :param dec_params: The decoder parameters
        """

        self._c = _C.VideoDecoder()
        ser_dec_params = dec_params.SerializeToString()
        self._c.open(sess._c, filename, ser_dec_params)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def close(self):
        """Closes the VideoDecoder."""
        self._c = None

    def next(self) -> Value:
        """
        Get the next frame from the video.

        Each frame is returned as an Exafunction Tensor value. Frames are stored
        in interleaved 8-bit RGB format.

        :return: The next frame
        :raises: StopIteration if there are no more frames
        """
        cc_frame = self._c.next_frame()  # May throw StopIteration
        return Value(cc_frame)

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self


class VideoEncoder:
    """
    VideoEncoder represents a remote video decoder.

    To use VideoEncoder, FfmpegEncode must be included in the placement group.
    """

    def __init__(
        self,
        sess: Session,
        filename: str,
        enc_params: ffmpeg_pb2.EncoderParameters,
        file_format: str = "",
    ):
        """
        Create a VideoEncoder from a video file.

        :param sess: The Exafunction session to use
        :param filename: The path to the video file
        :param enc_params: The encoder parameters
        :param file_format: The output file format to use. If empty, the file format
            is inferred from the filename.
        """
        self._c = _C.VideoEncoder()
        ser_enc_params = enc_params.SerializeToString()
        self._c.open(sess._c, filename, ser_enc_params, file_format)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def close(self):
        """Closes the VideoEncoder."""
        self._c.close()
        self._c = None

    def add_frame(self, frame: Value):
        """
        Add a frame to encode into the video.

        :param frame: The frame to add
        """
        self._c.add_frame(frame._c)
