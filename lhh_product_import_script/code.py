import codecs
import encodings.cp1250

__all__ = ['register']

ENCODING_NAME = "mssql_latin1"


class Codec(codecs.Codec):
    def encode(self, input_str, errors='strict'):
        return codecs.charmap_encode(input_str, errors, encoding_table)

    def decode(self, input_str, errors='strict'):
        return codecs.charmap_decode(input_str, errors, decoding_table)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input_str, final=False):
        return codecs.charmap_encode(input_str, self.errors, encoding_table)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input_str, final=False):
        return codecs.charmap_decode(input_str, self.errors, decoding_table)[0]


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(
        name=ENCODING_NAME,
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


table = list(encodings.cp1250.decoding_table)
table[0x90] = '\u0090'
decoding_table = ''.join(table)
encoding_table = codecs.charmap_build(decoding_table)


def search(name):
    if name == ENCODING_NAME:
        return getregentry()
    return None


def register():
    codecs.register(search)
