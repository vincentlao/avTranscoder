#include "InputStreamVideo.hpp"
#include "common.hpp"

extern "C" {
#ifndef __STDC_CONSTANT_MACROS
	#define __STDC_CONSTANT_MACROS
#endif
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#include <libavutil/pixdesc.h>
}

#include <iostream>
#include <stdexcept>

namespace avtranscoder
{

InputStreamVideo::InputStreamVideo()
	: m_codec         ( NULL )
	, m_codecContext  ( NULL )
	, m_frame         ( NULL )
	, m_selectedStream( -1 )
{}

InputStreamVideo::~InputStreamVideo()
{
	/*if( m_codecContext != NULL )
	{
		avcodec_close( m_codecContext );
		m_codecContext = NULL;
	}*/
	if( m_frame != NULL )
	{
		av_frame_free( &m_frame );
		m_frame = NULL;
	}
}

void InputStreamVideo::setup( const std::string& filename, const size_t streamIndex )
{
	av_register_all();

	InputFile::setup( filename );

	size_t videoStreamCount = 0;
	for( size_t streamId = 0; streamId < m_formatContext->nb_streams; streamId++ )
	{
		if( m_formatContext->streams[streamId]->codec->codec_type == AVMEDIA_TYPE_VIDEO )
		{
			if( videoStreamCount == streamIndex )
			{
				m_selectedStream = streamId;
			}
			videoStreamCount++;
		}
	}

	if( m_selectedStream == -1 )
	{
		throw std::runtime_error( "unable to find video stream" );
	}
	
	m_codec = avcodec_find_decoder( m_formatContext->streams[m_selectedStream]->codec->codec_id );
	if( m_codec == NULL )
	{
		throw std::runtime_error( "codec not supported" );
	}

	m_codecContext = avcodec_alloc_context3( m_codec );

	if( m_codecContext == NULL )
	{
		throw std::runtime_error( "unable to find context for codec" );
	}

	// if( codec->capabilities & CODEC_CAP_TRUNCATED )
	// 	codecContext->flags|= CODEC_FLAG_TRUNCATED;

	avcodec_open2( m_codecContext, m_codec, NULL );

	if( m_codecContext == NULL || m_codec == NULL )
	{
		throw std::runtime_error( "unable open codec" );
	}

	m_frame = avcodec_alloc_frame();
	if( m_frame == NULL )
	{
		throw std::runtime_error( "unable to setup frame buffer" );
	}
}

bool InputStreamVideo::readNextFrame( Image& frameBuffer )
{
	int got_frame = 0;

	while( ! got_frame )
	{
		AVPacket packet;
		av_init_packet( &packet );

		if( ! readNextPacket( packet, m_selectedStream ) ) // error or end of file
		{
			av_free_packet( &packet );
			return false;
		}

		avcodec_decode_video2( m_codecContext, m_frame, &got_frame, &packet );

		av_free_packet( &packet );
	}

	size_t decodedSize = avpicture_get_size( (AVPixelFormat)m_frame->format, m_frame->width, m_frame->height );
	if( frameBuffer.getBuffer().size() != decodedSize )
		frameBuffer.getBuffer().resize( avpicture_get_size( (AVPixelFormat)m_frame->format, m_frame->width, m_frame->height ) );

	// Copy pixel data from an AVPicture into one contiguous buffer.
	avpicture_layout( (AVPicture*)m_frame, (AVPixelFormat)m_frame->format, m_frame->width, m_frame->height, &frameBuffer.getBuffer()[0], frameBuffer.getBuffer().size() );

	return true;
}

}