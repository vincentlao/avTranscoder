#include "DataCodec.hpp"

namespace mediaengine
{
namespace mediaio
{

DataCodec::DataCodec( const ECodecType type, const std::string& codecName )
	: ICodec( type, codecName )
{
}

DataCodec::DataCodec( const ECodecType type, const AVCodecID codecId )
	: ICodec( type, codecId )
{
}

DataCodec::DataCodec( const ICodec& codec )
	: ICodec( codec )
{
}

}
}
