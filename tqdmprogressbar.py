def rclonecopyprocess(bot_msg, paths):
    RCLONE_PATH = '/usr/bin/rclone'
    cmd = [
        RCLONE_PATH,
        'copy',
        paths,
        'PD:/tele',
        '--progress',
        '--drive-chunk-size=16M',
        '--transfers=16',
        '--checkers=16',
        '--buffer-size=64M',
        ]
    checkfiles=[
        RCLONE_PATH,
        'check',
        paths,
        'PD:/tele',
        '--one-way',
        '-P',
        ]
    proch = Popen(checkfiles, stdout=PIPE, bufsize=1, universal_newlines=True,text=True)
    for line in proch.stdout:
        line=line.strip()
        if '0 differences found' in line:
            edit_text(bot_msg,'File Present in the cloud ☁')
            proch.kill()
            return
        else:
            pbar=tqdm(total=100, desc="Uploading to cloud ☁:", ncols=80,ascii="░▒",unit = 'B')
            proc = Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True,text=True)
            for line in proc.stdout:
                line = line.strip()
                # if '0 differences found' in line:
                # print(line)
                if line.startswith('*'):
                    percent = int(line.split(':')[1].split('%')[0])
                    if percent<100:
                        pbar.n = percent
                        pbar.refresh()
                        edit_text(bot_msg, pbar)
                    else:
                        edit_text(bot_msg,'Upload Finished!✅')
                        proc.kill()
                        return
