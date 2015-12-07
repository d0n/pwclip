#!/usr/bin/env python3



def drop_privileges(pid, real_only=False):
	'''Change user and group to match the given target process

	Normally that irrevocably drops privileges to the real user/group of the
	target process. With real_only=True only the real IDs are changed, but
	the effective IDs remain.
	'''
	if real_only:
		os.setregid(real_gid, -1)
		os.setreuid(real_uid, -1)
	else:
		os.setgid(real_gid)
		os.setuid(real_uid)
		assert os.getegid() == real_gid
		assert os.geteuid() == real_uid
	assert os.getgid() == real_gid
	assert os.getuid() == real_uid




