from __future__ import annotations
import os
import sys

try:
    import yt_dlp
except ImportError:
    print("ERROR: yt-dlp belum terinstall. Jalankan: pip install yt-dlp")
    sys.exit(1)

try:
    from rich.align import Align
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        DownloadColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
        TimeRemainingColumn,
        TransferSpeedColumn,
    )
    from rich.prompt import Prompt
    from rich.rule import Rule
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("ERROR: rich belum terinstall. Jalankan: pip install rich")
    sys.exit(1)


console = Console()

OUTPUT_DIR = "downloads"
BANNER = r"""
 __   __ _____ 
 \ \ / /|_   _| Build Version
  \ V /   | |   2.0.11
   | |    | |   Enjoy.
   |_|    |_|   @kitetsu67
"""

BANNER_TINY = "YT DOWNLOADER"

RESOLUTIONS = {
    "1": ("144p", 144),
    "2": ("240p", 240),
    "3": ("360p", 360),
    "4": ("480p", 480),
    "5": ("720p (HD)", 720),
    "6": ("1080p (Full HD)", 1080),
    "7": ("1440p (2K)", 1440),
    "8": ("2160p (4K)", 2160),
    "9": ("Best (tertinggi tersedia)", None),
}

AUDIO_QUALITIES = {
    "1": ("128 kbps", "128"),
    "2": ("192 kbps", "192"),
    "3": ("256 kbps", "256"),
    "4": ("320 kbps (terbaik)", "320"),
}


def print_banner() -> None:
    width = console.size.width
    subtitle = Text("YouTube Video & Shorts Downloader", style="bold cyan")
    tagline = Text("Powered by Iddant ID", style="italic dim")

    if width < 40:
        body = Group(
            Align.center(Text(BANNER_TINY, style="bold magenta")),
            Align.center(subtitle),
            Align.center(tagline),
        )
    else:
        body = Group(
            Align.center(Text(BANNER, style="bold magenta")),
            Align.center(subtitle),
            Align.center(tagline),
        )

    panel = Panel.fit(
        body,
        border_style="bright_magenta",
        padding=(0, 2),
    )
    console.print(panel)


def main_menu_table() -> Table:
    show_desc = console.size.width >= 60
    table = Table(
        show_header=True,
        header_style="bold white on blue",
        border_style="bright_blue",
        title_justify="center",
        expand=False,
    )
    table.add_column("No", justify="center", style="bold cyan", width=4)
    table.add_column("Pilihan", style="bold white")
    if show_desc:
        table.add_column("Deskripsi", style="dim")
        table.add_row("1", "[green]Download YouTube Video[/green]", "Video reguler")
        table.add_row("2", "[red]Download YouTube Short[/red]", "Short vertikal")
        table.add_row("3", "[bright_black]Keluar[/bright_black]", "Tutup aplikasi")
    else:
        table.add_row("1", "[green]Download YouTube Video[/green]")
        table.add_row("2", "[red]Download YouTube Short[/red]")
        table.add_row("3", "[bright_black]Keluar[/bright_black]")
    return table


def choices_table(title: str, choices: dict, accent: str = "cyan") -> Table:
    table = Table(
        show_header=True,
        header_style=f"bold white on {accent}",
        border_style=f"bright_{accent}" if accent in {"blue", "cyan", "magenta", "green", "red"} else accent,
        title_justify="center",
        expand=False,
    )
    table.add_column("No", justify="center", style=f"bold {accent}", width=4)
    table.add_column("Opsi", style="bold white")
    for key, (label, _) in choices.items():
        table.add_row(key, label)
    return table


def format_table() -> Table:
    show_desc = console.size.width >= 50
    table = Table(
        show_header=True,
        header_style="bold white on green",
        border_style="bright_green",
        title_justify="center",
        expand=False,
    )
    table.add_column("No", justify="center", style="bold green", width=4)
    table.add_column("Format", style="bold white")
    if show_desc:
        table.add_column("Keterangan", style="dim")
        table.add_row("1", "[bright_cyan]MP4[/bright_cyan]", "Video (gambar + suara)")
        table.add_row("2", "[bright_magenta]MP3[/bright_magenta]", "Audio saja")
    else:
        table.add_row("1", "[bright_cyan]MP4[/bright_cyan]")
        table.add_row("2", "[bright_magenta]MP3[/bright_magenta]")
    return table


def prompt_choice(table: Table, choices: dict, prompt_label: str = "Pilih nomor") -> str:
    console.print(table)
    return Prompt.ask(
        f"[bold yellow]{prompt_label}[/bold yellow]",
        choices=list(choices.keys()),
        show_choices=False,
    )


def prompt_url(kind: str) -> str:
    while True:
        url = Prompt.ask(f"\n[bold cyan]Masukkan URL {kind}[/bold cyan]").strip()
        if url:
            return url
        console.print("[red]URL tidak boleh kosong.[/red]")


def success(msg: str) -> None:
    console.print(f"[bold green]OK[/bold green]  {msg}")


def warn(msg: str) -> None:
    console.print(f"[bold yellow]![/bold yellow]   {msg}")


def error(msg: str) -> None:
    console.print(f"[bold red]X[/bold red]   {msg}")


def build_mp4_opts(max_height: int | None) -> dict:
    if max_height is None:
        fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
    else:
        fmt = (
            f"bestvideo[height<={max_height}][ext=mp4]+bestaudio[ext=m4a]/"
            f"bestvideo[height<={max_height}]+bestaudio/"
            f"best[height<={max_height}]"
        )
    return {
        "format": fmt,
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }


def build_mp3_opts(quality_kbps: str) -> dict:
    return {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality_kbps,
            }
        ],
    }


def download(url: str, ydl_opts: dict) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    max_url = max(10, console.size.width - 20)
    short_url = url if len(url) <= max_url else url[:max_url - 1] + "\u2026"

    narrow = console.size.width < 60
    columns = [
        SpinnerColumn(style="bright_magenta"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(
            bar_width=None if narrow else 40,
            complete_style="bright_green",
            finished_style="green",
        ),
        TextColumn("[bold yellow]{task.percentage:>5.1f}%[/bold yellow]"),
    ]
    if not narrow:
        columns += [DownloadColumn(), TransferSpeedColumn(), TimeRemainingColumn()]
    progress = Progress(*columns, console=console, transient=False)

    task_id = {"id": None, "title": "menunggu..."}

    def hook(d: dict) -> None:
        status = d.get("status")
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes") or 0
            info = d.get("info_dict") or {}
            title = info.get("title") or task_id["title"]
            task_id["title"] = title
            if task_id["id"] is None:
                task_id["id"] = progress.add_task(title[:50], total=total or None)
            else:
                if total and progress.tasks[task_id["id"]].total != total:
                    progress.update(task_id["id"], total=total)
                progress.update(task_id["id"], description=title[:50])
            progress.update(task_id["id"], completed=done)
        elif status == "finished":
            if task_id["id"] is not None:
                t = progress.tasks[task_id["id"]]
                progress.update(task_id["id"], completed=t.total or t.completed)

    ydl_opts = {**ydl_opts, "progress_hooks": [hook]}

    try:
        with progress:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        success(f"Selesai. File tersimpan di folder: [bold]{OUTPUT_DIR}/[/bold]")
    except yt_dlp.utils.DownloadError as exc:
        error(f"Gagal download: {exc}")
    except KeyboardInterrupt:
        warn("Download dibatalkan oleh user.")
    except Exception as exc:  # noqa: BLE001
        error(f"Error tak terduga: {exc}")

def handle_download(kind: str) -> None:
    url = prompt_url(kind)

    fmt_choice = prompt_choice(format_table(), {"1": ("MP4", None), "2": ("MP3", None)},
                               prompt_label="Pilih format")

    if fmt_choice == "1":
        res_sel = prompt_choice(
            choices_table("PILIH RESOLUSI VIDEO", RESOLUTIONS, accent="cyan"),
            RESOLUTIONS,
            prompt_label="Pilih resolusi",
        )
        _, max_height = RESOLUTIONS[res_sel]
        opts = build_mp4_opts(max_height)
    else:
        q_sel = prompt_choice(
            choices_table("PILIH KUALITAS AUDIO (MP3)", AUDIO_QUALITIES, accent="magenta"),
            AUDIO_QUALITIES,
            prompt_label="Pilih kualitas",
        )
        _, kbps = AUDIO_QUALITIES[q_sel]
        opts = build_mp3_opts(kbps)

    download(url, opts)


def main() -> None:
    while True:
        console.clear()
        print_banner()
        console.print(main_menu_table())
        choice = Prompt.ask(
            "\n[bold yellow]Pilih menu[/bold yellow]",
            choices=["1", "2", "3"],
            show_choices=False,
        )

        if choice == "1":
            handle_download("YouTube Video")
        elif choice == "2":
            handle_download("YouTube Short")
        elif choice == "3":
            console.print(Panel.fit(
                "[bold cyan]Terima kasih, sampai jumpa![/bold cyan]",
                border_style="bright_cyan",
            ))
            break

        Prompt.ask("\n[dim]Tekan Enter untuk kembali ke menu...[/dim]", default="")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Terimakasi udah close program saya ya.[/bold yellow]")
