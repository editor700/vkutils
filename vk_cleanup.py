#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vk_api
import sys

LOGIN = 'login'
PASSWORD = 'password'

def prt(msg, *args, **kwargs):
	sys.stdout.write(msg.format(*args, **kwargs))
	sys.stdout.flush()

def main():
	session = vk_api.VkApi(LOGIN, PASSWORD)
	print('Start VK cleaner...')
	prt('Logging in... ')
	try:
		session.auth()
	except vk_api.AuthorizationError as error_msg:
		print(error_msg)
		return
	vk = session.get_api()
	userInfo = vk.users.get()
	prt('ok: {} {}', userInfo[0]['first_name'], userInfo[0]['last_name'])
	prt('\n')
	print('Start clieaning VK profile...')
	# Clean black list
	prt('Clean black list... ')
	while True:
		blackList = vk.account.getBanned()
		for u in blackList['items']:
			vk.account.unbanUser(user_id=u['id'])
		if len(blackList['items'])==0:
			break
	prt('ok\n')
	# Clean profile
	prt('Clear profile... ')
	vk.account.saveProfileInfo(relation=0, bdate_visibility=0, home_town='', country_id=0, city_id=0, status='')
	while True:
		docs = vk.docs.get()
		for d in docs['items']:
			vk.docs.delete(owner_id=int(session.token['user_id']), doc_id=d['id'])
		if len(docs['items'])==0:
			break
	prt('ok\n')
	# Clean faves
	prt('Clean fave links... ')
	while True:
		links = vk.fave.getLinks()
		for l in links['items']:
			vk.fave.removeLink(link_id=l['id'])
		if len(links['items'])==0:
			break
	prt('ok\n')
	prt('Clean fave users... ')
	while True:
		users = vk.fave.getUsers()
		for u in users['items']:
			vk.fave.removeUser(user_id=u['id'])
		if len(users['items'])==0:
			break
	prt('ok\n')
	# Unlike
	prt('Clean liked videos... ')
	while True:
		videos = vk.fave.getVideos()
		for v in videos['items']:
			vk.likes.delete(type='video', owner_id=v['owner_id'], item_id=v['id'])
		if len(videos['items'])==0:
			break
	prt('ok\n')
	prt('Clean liked posts... ')
	while True:
		posts = vk.fave.getPosts()
		for p in posts['items']:
			vk.likes.delete(type='post', owner_id=p['owner_id'], item_id=p['id'])
		if len(posts['items'])==0:
			break
	prt('ok\n')
	prt('Clean liked photos... ')
	while True:
		photos = vk.fave.getPhotos()
		for p in photos['items']:
			vk.likes.delete(type='photo', owner_id=p['owner_id'], item_id=p['id'])
		if len(photos['items'])==0:
			break
	prt('ok\n')
	# Remove friend list
	prt('Clean friend list... ')
	friends = vk.friends.get()
	for f in friends['items']:
		vk.friends.delete(user_id=f)
	prt('ok\n')
	# Remove photos
	prt('Remove photo albums... ')
	while True:
		albums = vk.photos.getAlbums(album_ids=0)
		for a in albums['items']:
			vk.photos.deleteAlbum(album_id=a['id'])
		if len(albums['items'])==0:
				break
	prt('ok\n')
	prt('Remove photos... ')
	while True:
		photos = vk.photos.getAll()
		for p in photos['items']:
			vk.photos.delete(photo_id=p['id'])
		if len(photos['items'])==0:
			break
	prt('ok\n')
	# Remove videos
	prt('Remove video albums... ')
	while True:
		videos = vk.video.getAlbums()
		for v in videos['items']:
			vk.video.deleteAlbum(album_id=v['id'])
		if len(videos['items'])==0:
			break
	prt('ok\n')
	prt('Remove videos... ')
	while True:
		videos = vk.video.get()
		for v in videos['items']:
			vk.video.delete(target_id=int(session.token['user_id']), owner_id=v['owner_id'], video_id=v['id'])
		if len(videos['items'])==0:
			break
	prt('ok\n')
	# Exit from groups
	prt('Clear groups... ')
	while True:
		groups = vk.groups.get()
		for g in groups['items']:
			vk.groups.leave(group_id=g)
		if len(groups['items'])==0:
			break
	prt('ok\n')
	# Remove wall posts
	prt('Remove wall posts... ')
	while True:
		wall = vk.wall.get()
		for p in wall['items']:
			vk.wall.delete(post_id=p['id'])
		if len(wall['items'])==0:
			break
	prt('ok\n')
	# Exit dialogs
	# Clean dialogs
	prt('Clear dialog list... ')
	while True:
		messages = vk.messages.getDialogs()
		for d in messages['items']:
			if d.get('message')!=None:
				if d['message'].get('chat_id')!=None:
					vk.messages.removeChatUser(chat_id=d['message']['chat_id'], user_id=int(session.token['user_id']))
					vk.messages.deleteDialog(peer_id=2000000000+d['message']['chat_id'])
				elif d['message'].get('user_id')!=None:
					vk.messages.deleteDialog(user_id=d['message']['user_id'])
		if len(messages['items'])==0:
			break
	prt('ok\n')
	# Clean notes
	prt('Clear notes... ')
	while True:
		notes = vk.notes.get()
		for n in notes['items']:
			vk.notes.delete(note_id=n['id'])
		if len(notes['items'])==0:
			break
	prt('ok\n')
	# Clean audios
	print('Cleaning complete.')
	print('Audio must be cleaned manually by executing JavaScript code located in file clean_audio.js in your browser console on page https://vk.com/audios.')

if __name__=='__main__':
	main()