
import discord
import re



def _hydrate_user_mentions(text: str, guild: discord.Guild | None, author: discord.abc.User) -> str:
    if not guild:
        return text

    # Ensure the message author can always be tagged even if guild cache is partial.
    cached_members: list[discord.abc.User] = list(guild.members)
    if author not in cached_members:
        cached_members.append(author)

    def repl(match: re.Match[str]) -> str:
        handle = match.group(1)
        punct = match.group(2)
        clean = handle.strip().lower()

        if clean in {"everyone", "here"}:
            return match.group(0)

        member = next(
            (
                m for m in cached_members
                if clean in {
                    m.name.lower(),
                    m.display_name.lower(),
                    (m.global_name or "").lower(),
                }
            ),
            None,
        )
        return f"{member.mention}{punct}" if member else match.group(0)

    return re.sub(r"@([A-Za-z0-9_.-]{2,32})([.,:;!?]?)", repl, text)
