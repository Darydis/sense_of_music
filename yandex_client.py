from yandex_music import Client

client = Client().init()

def get_playlist(username: str, playlist_id: str) -> str:
    # Правильный вызов метода клиента
    pl = client.users_playlists(kind=playlist_id, user_id=username)  # или: client.users_playlists(playlist_id, username)

    lines = []
    for item in pl.tracks:
        track = item.track
        artists = ', '.join(a.name for a in track.artists)
        lines.append(f"{artists} – {track.title}")

    if not lines:
        return "📭 Плейлист пуст или не найден."

    # Объединяем в один текст
    return "\n".join(lines)