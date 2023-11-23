from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# # remove axes ticks globally parameters
plt.rcParams["xtick.bottom"] = False
plt.rcParams["xtick.labelbottom"] = False
plt.rcParams["xtick.top"] = False
plt.rcParams["xtick.labeltop"] = False
plt.rcParams["ytick.left"] = False
plt.rcParams["ytick.labelleft"] = False
plt.rcParams["ytick.right"] = False
plt.rcParams["ytick.labelright"] = False

# reserve more memort to matplotlib for faster animation
plt.rcParams["animation.embed_limit"] = 2**512

# Given omega = 2 * pi * f
t = np.arange(-1, 1, 0.01)
f = np.arange(1, 32, 1)
omega = 2 * np.pi * f

complex_nums = np.exp(1j * omega[2] * t)

A = np.abs(complex_nums)
phi = np.arctan2(np.imag(complex_nums), np.real(complex_nums))


fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(131)
ax1.set_title("F(w)")


ax2 = fig.add_subplot(132)
ax2.set_title("f(t) = exp(iwt)")


ax3 = fig.add_subplot(133)
ax3.set_title("Complex phasor")
ax3.set_xlim(-1, 1)
ax3.set_ylim(-1, 1)
ax3.set_aspect("equal")
ax3.grid(False)
ax3.set_xlabel("Real")
ax3.set_ylabel("Imaginary")


phase_slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
Amplitude_slider_ax = plt.axes([0.25, 0.05, 0.65, 0.03])
phase_slider = Slider(
    ax=phase_slider_ax,
    label="Phase",
    valmin=0,
    valmax=2 * np.pi,
    valinit=0,
    valstep=np.pi / 10,
)

Amplitude_slider = Slider(
    ax=Amplitude_slider_ax,
    label="Amplitude",
    valmin=0,
    valmax=1,
    valinit=0.5,
    valstep=0.1,
)
Omega_slider_ax = plt.axes([0.25, 0.15, 0.65, 0.03])
Omega_slider = Slider(
    ax=Omega_slider_ax,
    label="Omega",
    valmin=0,
    valmax=2 * np.pi * 32,
    valstep=2 * np.pi,
    valinit=2 * np.pi,
)


def update_frame(frame, total_frames):
    # Divide the total frames into three equal parts for phase, amplitude, and omega
    segment_length = total_frames // 3
    segment_index = frame // segment_length
    frame_in_segment = frame % segment_length

    if segment_index == 0:
        if frame_in_segment < segment_length / 2:
            # First segment: Change phase from -pi to pi
            new_phase = np.pi * (frame_in_segment / segment_length)
            # phase_slider.set_val(new_phase)
        else:
            new_phase = np.pi - np.pi * (frame_in_segment / segment_length)

        phase_slider.set_val(new_phase)
    elif segment_index == 1:
        # Second segment: Change amplitude from 1 to 0 and back to 1
        if frame_in_segment < segment_length / 2:
            new_amplitude = 0.5 - frame_in_segment / segment_length
        else:
            new_amplitude = (frame_in_segment / segment_length) - 0.5
        Amplitude_slider.set_val(new_amplitude)
    elif segment_index == 2:
        # Third segment: Change omega from -pi to pi
        if frame_in_segment < segment_length / 2:
            new_omega = 3 * np.pi * (frame_in_segment / segment_length)
        else:
            new_omega = 3 * np.pi * (frame_in_segment / segment_length) - 2 * np.pi
        Omega_slider.set_val(new_omega)

    # Update the plot
    update_plot(None)


def update_plot(val):
    sinosoid = Amplitude_slider.val * np.exp(
        1j * (Omega_slider.val * t + phase_slider.val)
    )
    phasor = Amplitude_slider.val * np.exp(1j * phase_slider.val)

    ax1.clear()
    ax2.clear()
    ax3.clear()
    # ax1.plot(2 * np.pi * 32, 0, color="black")
    ax1.axvline(Omega_slider.val, color="blue", linestyle="--")
    ax1.set_title("F(w)")
    # ax1.set_xlim(0, 2 * np.pi * (32 / 10))
    ax1.set_ylim(0, 10)
    ax2.plot(t, np.real(sinosoid), color="green")
    ax2.plot(t, np.imag(sinosoid), color="purple")

    ax1.set_aspect("equal")
    ax2.set_title("f(t) = exp(iwt)")
    ax1.set_xlim(0, 2 * np.pi * 32)
    ax2.set_xlim(-1, 1)
    ax2.set_ylim(-1, 1)
    ax2.set_aspect("equal")
    ax3.set_title("Complex phasor")
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)
    ax3.set_aspect("equal")
    ax3.grid(False)
    ax3.set_xlabel("Real")
    ax3.set_ylabel("Imaginary")
    ax3.arrow(
        0,
        0,
        np.real(phasor),
        np.imag(phasor),
        head_width=0.05,
        head_length=0.1,
        fc="k",
        ec="k",
    )

    fig.canvas.draw_idle()


phase_slider.on_changed(update_plot)
Amplitude_slider.on_changed(update_plot)
Omega_slider.on_changed(update_plot)


# ======= uncomment this section to animate on predefined slider values and save the animation to mp4 file ==========
# total_frames = 300  # Example total frames
# ani = FuncAnimation(
#     fig,
#     lambda frame: update_frame(frame, total_frames),
#     frames=total_frames,
#     blit=False,
# )
# ani.save("FT_1D.mp4", writer="ffmpeg", fps=30)


plt.show()
