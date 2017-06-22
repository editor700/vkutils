/*
 * Audio must be cleaned manually by executing following JavaScript code in your browser console on page https://vk.com/audio
 */
a = document.getElementsByClassName('audio_row');
for (var i = 0; i < a.length; i++) AudioUtils.deleteAudio(a[i], AudioUtils.getAudioFromEl(a[i], true));
