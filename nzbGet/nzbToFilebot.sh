#!/bin/sh 

##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Filebot Script
#
# This script will send the unarchived file to filebot for further
# processing. The script will recognize the following categories:
# Series
# TV
# Movie
# Movies

### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94
POSTPROCESS_SKIPPED=95

if [ "$NZBPP_PARSTATUS" -eq 1 -o "$NZBPP_UNPACKSTATUS" -eq 1 ]; then
  echo "[WARNING] This nzb-file has failure status (par-check or unpack failed)"
  exit $POSTPROCESS_SKIPPED
fi

CATEGORY=$(echo "$NZBPP_CATEGORY" | awk '{print tolower($0)}')

_split() {
  STATUS=$?
  echo "[INFO] $1"
  METHOD=$(echo "$1" | awk -F'[][]' '{print $2}')
  REST==$(echo "$1"| sed -e "s/\[$METHOD\]//g")
  FROM=$(echo "$REST" | awk -F'[][]' '{print $2}')
  ESCAPED=$(echo "$FROM" | sed -e 's/[\/&]/\\&/g')
  REST==$(echo "$REST"| sed -e "s/\[$ESCAPED\]//g")
  TO=$(echo "$REST" | awk -F'[][]' '{print $2}')
}

if [ "$CATEGORY" == "series" ] || [ "$CATEGORY" == "tv" ]; then
  echo "[INFO] Queringy for tv shows"
  OUTPUT=$(filebot -script fn:amc "$NZBPP_DIRECTORY" -r --output /volume1 --log info --conflict override --action MOVE -non-strict --def "seriesFormat=Serien/{n.replaceTrailingBrackets().replaceAll(': ', ' - ').replaceAll('/[\`´‘’ʻ]/', '\'').space(' ')}{' (' + y + ')'}/{episode.special ? 'Specials' : 'Season '+s.pad(2) + {' (' + episodelist.findAll{ it.season == s }.airdate.year.min() + ')'}.call()}/{n.replaceAll(': ', ' - ').replaceAll('[\`´‘’ʻ]', '\'').space(' ')} - {episode.special ? '0x'+special.pad(2) : sxe} - {t.replaceAll('[!?,]+', '').replaceAll(': ', ' - ').replaceAll('[\`´‘’ʻ]', '\'').space(' ')}{'.'+vf}{'.'+source}{'.'+vc.replace('Microsoft', 'VC-1')}{audios.size() > 1? '.DL.'+audios.groupBy{ it.Codec }.collect{ c, a -> [c] + a*.Language }.flatten().join('.') : '.'+ac.replace('MPEG Audio', 'MP3')}{audios.size() == 1? {try{'.' + allOf{audios.language}{videos.language}.flatten().first()} catch(Exception x){'.en'}}.call() : ''}{'.' + audios.channels.sort().last().replace('8', '7.1').replace('7', '6.1').replace('6', '5.1').replace('3', '2.1').replace('2','2.0')}")
  _split "$OUTPUT"
elif [ "$CATEGORY" == "movies" ] || [ "$CATEGORY" == "movie" ]; then
  echo "[INFO] Querying for movies"
  OUTPUT=$(filebot -script fn:amc "$NZBPP_DIRECTORY" -r --output /volume1 --log info --conflict override --action MOVE -non-strict --def "movieFormat=Movies/{n.replaceTrailingBrackets().replaceAll(': ', ' - ').replaceAll('/[\`´‘’ʻ]/', '\'').space(' ')}{' (' + y + ')'}{fn.match(/(?i)sbs/)? '.3D-SBS': ''}{'.'+vf}{'.'+source}{'.'+vc.replace('Microsoft', 'VC-1')}{audios.size() > 1? '.DL.'+audios.groupBy{ it.Codec }.collect{ c, a -> [c.replace('MPEG Audio', 'MP3')] + a*.Language }.flatten().join('.') : '.'+ac.replace('MPEG Audio', 'MP3')}{audios.size() == 1? {try{'.' + allOf{audios.language}{videos.language}.flatten().first()} catch(Exception x){'.de'}}.call() : ''}{'.' + audios.channels.sort().last().replace('8', '7.1').replace('7', '6.1').replace('6', '5.1').replace('3', '2.1').replace('2','2.0')}")
  _split "$OUTPUT"
else
  echo "[WARNING] Did not recognize category $NZBPP_CATEGORY"
  exit $POSTPROCESS_SKIPPED
fi

if [ $STATUS -eq 0 ];then
  exit $POSTPROCESS_SUCCESS
else
  echo "[WARNING] Filebot script failed"
  exit $POSTPROCESS_SKIPPED
fi
