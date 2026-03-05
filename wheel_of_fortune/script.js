// Tier Data Configuration
const tiers = {
    silver: {
        name: "Silver (1500+)",
        color: "#C0C0C0", // Silver
        prizes: [
            "Free Pre-Roll",
            "5% Off Purchase",
            "Glass Pipe",
            "Lighter",
            "One Hit Wonder Puff",
            "Exclusive Strain Sample",
            "5,000 Loyalty Points",
            "Canni Water",
            "Hot or Cold Drink",
            "Snack (Chips/Choc)"
        ]
    },
    gold: {
        name: "Gold (2500+)",
        color: "#FFD700", // Gold
        prizes: [
            "10% Off Purchase",
            "Exclusive Strain Sample",
            "One Hit Wonder Puff",
            "One Hit Wonder Capsule",
            "Bucket Hat",
            "Free Pre-Roll",
            "10,000 Loyalty Points",
            "Hot/Cold Infused Drink",
            "Snack (Chips/Choc)",
            "Lighter"
        ]
    },
    platinum: {
        name: "Platinum (3500+)",
        color: "#E5E4E2", // Platinum
        prizes: [
            "Infused Drink",
            "Exclusive Strain Sample",
            "Bucket Hat",
            "15% Off Purchase",
            "15,000 Loyalty Points",
            "Free Moonstick",
            "30mg Rosin Capsule",
            "20mg Edibles",
            "Dab Hit",
            "Free Pre-Roll Indoor"
        ]
    }
};

// State
let currentTier = null;
let isSpinning = false;
let wheelRotation = 0;

// DOM Elements
const tierSelectionScreen = document.getElementById('tier-selection');
const wheelScreen = document.getElementById('wheel-screen');
const wheelElement = document.getElementById('wheel');
const resultModal = document.getElementById('result-modal');
const resultPrizeText = document.getElementById('result-prize');
const spinBtn = document.getElementById('spin-btn');

// -- Functions --

function selectTier(tierKey) {
    currentTier = tiers[tierKey];
    showScreen(wheelScreen);
    setupWheel();
}

function showScreen(screenElement) {
    document.querySelectorAll('.screen').forEach(el => el.classList.add('hidden'));
    screenElement.classList.remove('hidden');
}

function resetToTiers() {
    currentTier = null;
    isSpinning = false;
    wheelRotation = 0;
    wheelElement.style.transition = 'none';
    wheelElement.style.transform = `rotate(0deg)`;
    resultModal.classList.add('hidden');
    spinBtn.disabled = false;
    showScreen(tierSelectionScreen);
}

function setupWheel() {
    wheelElement.innerHTML = ''; // Clear existing
    const prizeCount = currentTier.prizes.length;
    const sliceAngle = 360 / prizeCount;

    // 1. Create Conic Gradient Background
    let gradientParts = [];
    currentTier.prizes.forEach((_, index) => {
        const start = index * sliceAngle;
        const end = (index + 1) * sliceAngle;
        const color = index % 2 === 0 ? '#2a2a2a' : '#1a1a1a';
        gradientParts.push(`${color} ${start}deg ${end}deg`);
    });
    wheelElement.style.background = `conic-gradient(${gradientParts.join(', ')})`;

    // 2. Add Text Labels using Polar Coordinates
    const wheelRadius = wheelElement.clientWidth / 2;
    // We want the text to start partially out from center to avoid clutter at pivot
    const textOffset = wheelRadius * 0.15;

    currentTier.prizes.forEach((prize, index) => {
        const textEl = document.createElement('div');
        textEl.classList.add('wheel-text');
        textEl.textContent = prize;

        // Calculate the center angle of the slice
        // Slice 0 starts at 0deg (Top, due to conic-gradient standard) to sliceAngle.
        // Center is (index + 0.5) * sliceAngle.
        const midAngle = (index + 0.5) * sliceAngle;

        // Transform Logic:
        // 1. Rotate to align with the slice angle.
        //    Standard CSS Text flow is Horizontal (0deg = Right).
        //    We want Text flow to point UP (0deg = Top) if we didn't rotate. 
        //    So `rotate(-90deg)` aligns text to Point "Up".
        //    Then `rotate(midAngle)` points it to the slice direction.
        //    Total Rotation `R = midAngle - 90`.
        // 
        // 2. Translate OUT along that direction.
        //    `translate(radius)` happens in the local rotated coordinate system.
        // 
        // So: `rotate(R) translate(offset)` should work.

        textEl.style.transform = `rotate(${midAngle - 90}deg) translate(${wheelRadius * 0.55}px)`; // Translate to mid-radius roughly

        // Fix for readability? 
        // If the text is upside down (angles 90-270), we might want to flip it?
        // Usually wheel text reads from center outward, so it's always "sideways" but consistent.
        // The user prompted: "Each prize label MUST be perfectly centred on the midline of its slice."

        wheelElement.appendChild(textEl);
    });
}

function spinWheel() {
    if (isSpinning) return;
    isSpinning = true;
    spinBtn.disabled = true;

    const prizeCount = currentTier.prizes.length;
    const sliceAngle = 360 / prizeCount;

    // 1. Random Selection
    const randomIndex = Math.floor(Math.random() * prizeCount);
    const selectedPrize = currentTier.prizes[randomIndex];

    // 2. Calculate Rotation
    // Target is mid-line of the selected slice.
    // Pointer is at Top (0deg).
    // Slice `randomIndex` center is at `(randomIndex + 0.5) * sliceAngle`.
    const midAngle = (randomIndex + 0.5) * sliceAngle;

    const spinCount = 5 + Math.floor(Math.random() * 5); // 5-10 spins
    const jitter = (Math.random() - 0.5) * (sliceAngle * 0.2); // Keep jitter small to hit near center

    // We want to arrive at a rotation R such that:
    // (RotatedWheel Angle at Top) = midAngle ? No.
    // If Wheel is at 0deg, Slice 0 is at Top.
    // If we want Slice X at Top, we must rotate Wheel by -AngleOfSliceX.

    // Target position: -midAngle (CCW rotation brings angle to top).
    // We want CW spinning (positive).
    // So target = 360*spins + (360 - midAngle).

    let targetRotation = 360 * spinCount + (360 - midAngle) + jitter;

    // Add to current rotation to keep continuous
    // We need to calculate the *delta* needed. 
    // Just adding `targetRotation` to `wheelRotation` isn't enough, 
    // because `wheelRotation` effectively holds our current "zero".

    // Better approach:
    // Reset internal tracker to 0-360 representation? No, visual glitch.

    // `currentAbsRotation = wheelRotation`.
    // We want final `wheelRotation` to satisfy `wheelRotation % 360 == (360 - midAngle)`.

    // `nextRotation = wheelRotation + minSpins + delta`
    const currentMod = wheelRotation % 360;
    // We want to get to `targetMod = 360 - midAngle`.
    // Distance forward = (targetMod - currentMod + 360) % 360.

    const rotationNeeded = (360 - midAngle - currentMod + 360) % 360;
    const totalRotation = wheelRotation + (360 * spinCount) + rotationNeeded + jitter;

    wheelRotation = totalRotation;

    // Apply CSS
    // Re-enable transition (in case it was removed by reset)
    wheelElement.style.transition = 'transform 4s cubic-bezier(0.15, 0, 0.2, 1)';
    wheelElement.style.transform = `rotate(${wheelRotation}deg)`;

    // 3. Show Result
    setTimeout(() => {
        isSpinning = false;
        resultPrizeText.textContent = selectedPrize;
        resultModal.classList.remove('hidden');
        fireConfetti();
    }, 4000);
}

function spinAgain() {
    isSpinning = false;
    spinBtn.disabled = false;
    resultModal.classList.add('hidden');
    // We do NOT reset rotation here, so it spins naturally from current position
}

function fireConfetti() {
    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: [currentTier.color, '#ffffff', '#00ff00']
    });
}
