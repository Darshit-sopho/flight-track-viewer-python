from ftv import run

R = run(
    animate=True,
    animate_step_seconds=30,
    save_figures_enabled=True,
    save_video_enabled=True,
)

print("Outputs:", R.get("outputs", {}))
