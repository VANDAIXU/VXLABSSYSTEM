<!DOCTYPE html>
<html lang="en" class="scroll-smooth">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VX STUDIA - Generative Cinema</title>

    <script src="https://cdn.tailwindcss.com"></script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;800&family=Orbitron:wght@400;700&display=swap"
        rel="stylesheet">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/simplex-noise/2.4.0/simplex-noise.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>


    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        'sans': ['Inter', 'sans-serif'],
                        'orbitron': ['Orbitron', 'sans-serif'],
                    },
                    colors: {
                        'void': '#000000',
                        'light': '#FFFFFF',
                        'grey': '#888888',
                        'border': '#222222',
                        'primary': '#00bfff', 
                    },
                    animation: {
                        'fade-in': 'fade-in 0.5s ease-out forwards',
                        'spin': 'spin 1s linear infinite',
                        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'typing-dot': 'typing-dot 1.4s infinite both',
                    },
                    keyframes: {
                        'fade-in': {
                            '0%': { opacity: '0', transform: 'translateY(10px)' },
                            '100%': { opacity: '1', transform: 'translateY(0)' },
                        },
                         'spin': {
                            'from': { transform: 'rotate(0deg)' },
                            'to': { transform: 'rotate(360deg)' },
                        },
                        'pulse': {
                            '0%, 100%': { opacity: '1' },
                            '50%': { opacity: '.5' },
                        },
                        'typing-dot': {
                            '0%': { transform: 'scale(1)' },
                            '15%': { transform: 'scale(1)' },
                            '25%': { transform: 'scale(1.3)' },
                            '35%': { transform: 'scale(1)' },
                        }
                    }
                }
            }
        }
    </script>

    <style>
        body {
            background-color: #000;
            overflow-x: hidden;
        }

        #flow-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
        }

        .content-wrapper {
            position: relative;
            z-index: 2;
        }

        .header-glass {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid #222222;
        }

        .btn {
            @apply px-6 py-2.5 font-medium rounded-full transition-all duration-300 ease-in-out;
        }

        .btn-light {
            @apply bg-light text-void hover:bg-opacity-80 transform hover:scale-105;
        }

        .btn-outline {
            @apply border border-border text-grey hover:text-light hover:border-light;
        }

        .fade-in-section {
            opacity: 0;
            transform: translateY(25px);
            transition: opacity 0.8s ease-out, transform 0.8s ease-out;
            transition-delay: 0.2s;
        }

        .fade-in-section.is-visible {
            opacity: 1;
            transform: translateY(0);
        }

        #veo-script-output,
        #vx-script-output,
        #consa-script-output,
        #vision-script-output {
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .loader {
            border: 2px solid #222222;
            border-top: 2px solid #FFFFFF;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }

        .selectable-card {
            @apply bg-void border border-border rounded-lg p-3 text-center cursor-pointer transition-all duration-300 h-full flex items-center justify-center;
        }

        .selectable-card:hover,
        .selectable-card.selected {
            @apply border-light transform -translate-y-1;
        }

        .selectable-card.selected {
            @apply bg-white/5;
        }

        .prompt-section-heading {
            @apply text-2xl font-bold text-light mb-4 text-center font-orbitron;
        }

        .sub-heading {
            @apply text-lg font-semibold text-primary mb-3 block;
        }

        .selection-tag {
            @apply inline-flex items-center bg-border text-light text-sm font-medium mr-2 mb-2 px-3 py-1.5 rounded-full;
        }

        .selection-tag button {
            @apply ml-2 text-grey hover:text-light transition-colors duration-200 text-lg leading-none;
        }

        .selection-tag-director {
            @apply bg-red-900/50 border border-red-700;
        }

        .selection-tag-style {
            @apply bg-blue-900/50 border border-blue-700;
        }

        .selection-tag-effect {
            @apply bg-purple-900/50 border border-purple-700;
        }

        .selection-tag-motion {
            @apply bg-green-900/50 border border-green-700;
        }

        .story-scene {
            @apply bg-black/20 border border-border p-4 rounded-lg mb-4;
        }

        /* Pricing Card Styles */
        .pricing-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid #222222;
            transition: all 0.3s ease-in-out;
        }

        .pricing-card:hover {
            transform: translateY(-8px);
            border-color: #00bfff;
            background: rgba(0, 191, 255, 0.05);
        }

        .pricing-card-highlight {
            border-color: #00bfff;
            transform: scale(1.05);
        }

        .pricing-card ul li svg {
            @apply text-primary;
        }

        /* VX Libro New UI Styles */
        #vx-libro-page {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .libro-chat-container {
            width: 100%;
            max-width: 800px;
            height: 80vh;
            max-height: 800px;
            background: rgba(10, 10, 10, 0.5);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid #222;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        #libro-chat-log {
            flex-grow: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .libro-message {
            display: flex;
            gap: 12px;
            max-width: 90%;
        }

        .libro-message.user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }

        .libro-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            background-color: #222;
        }

        .libro-message-content {
            padding: 12px 16px;
            border-radius: 12px;
            background-color: rgba(30, 30, 30, 0.7);
            color: #E5E7EB;
        }

        .libro-message.user .libro-message-content {
            background-color: rgba(0, 191, 255, 0.2);
        }

        .libro-message-content p,
        .libro-message-content ul,
        .libro-message-content ol,
        .libro-message-content pre {
            margin-bottom: 8px;
        }

        .libro-message-content p:last-child {
            margin-bottom: 0;
        }

        .libro-message-content code {
            background-color: rgba(0, 0, 0, 0.3);
            padding: 2px 4px;
            border-radius: 4px;
            font-family: monospace;
        }

        .libro-message-content pre {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
            position: relative;
        }

        .libro-message-content pre code {
            padding: 0;
            background: none;
        }

        .copy-code-btn {
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: #ccc;
            padding: 4px;
            border-radius: 4px;
            cursor: pointer;
            opacity: 0.5;
            transition: opacity 0.2s;
        }

        .libro-message-content pre:hover .copy-code-btn {
            opacity: 1;
        }

        .libro-typing-indicator {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background-color: #555;
            border-radius: 50%;
            animation: typing-dot 1.4s infinite both;
        }

        .typing-dot:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-dot:nth-child(3) {
            animation-delay: 0.4s;
        }

        #libro-input-form {
            padding: 16px;
            border-top: 1px solid #222;
            display: flex;
            gap: 12px;
            align-items: center;
        }

        #libro-prompt-textarea {
            flex-grow: 1;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid #333;
            border-radius: 8px;
            padding: 10px 16px;
            color: #fff;
            resize: none;
            min-height: 48px;
            max-height: 200px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.2s;
        }

        #libro-prompt-textarea:focus {
            border-color: #00bfff;
        }

        #libro-submit-button {
            width: 48px;
            height: 48px;
            flex-shrink: 0;
            background: #00bfff;
            border-radius: 8px;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        #libro-submit-button:hover {
            background-color: rgba(0, 191, 255, 0.8);
        }

        #libro-submit-button:disabled {
            background-color: #333;
            cursor: not-allowed;
        }

        #libro-clear-chat {
            position: absolute;
            top: 24px;
            right: 24px;
            background: rgba(255, 255, 255, 0.1);
            color: #aaa;
            border: 1px solid #333;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 50;
            transition: all 0.2s;
        }

        #libro-clear-chat:hover {
            color: #fff;
            border-color: #fff;
            transform: rotate(90deg);
        }
    </style>
</head>

<body class="antialiased">

    <canvas id="flow-canvas"></canvas>

    <div class="content-wrapper">

        <header id="header" class="fixed w-full z-30 transition-all duration-300 ease-in-out">
            <div class="max-w-7xl mx-auto px-6">
                <div class="flex items-center justify-between h-24">
                    <div class="flex-shrink-0">
                        <a href="#" id="home-link" class="text-3xl font-bold tracking-widest text-light font-orbitron"
                            aria-label="VX STUDIA">
                            VX STUDIA
                        </a>
                    </div>
                    <div id="nav-controls" class="flex items-center gap-6">
                        <a href="#contact" class="btn btn-outline text-sm hidden md:block">Start a Project</a>
                        <div class="relative">
                            <button id="menu-button" aria-label="Open Menu" class="text-grey hover:text-light transition-colors">
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
                                </svg>
                            </button>
                            <div id="dropdown-menu"
                                class="hidden absolute right-0 mt-2 w-48 bg-black/80 backdrop-blur-md border border-border rounded-lg shadow-lg py-2 z-50">
                                <a href="#" id="vx-labs-link"
                                    class="block px-4 py-2 text-sm text-grey hover:bg-border hover:text-light">VX
                                    LABS</a>
                                <a href="#" id="vx-authority-link"
                                    class="block px-4 py-2 text-sm text-grey hover:bg-border hover:text-light">VX
                                    Authority</a>
                                <a href="#" id="vx-consa-link"
                                    class="block px-4 py-2 text-sm text-grey hover:bg-border hover:text-light">VX
                                    Consa</a>
                                <a href="#" id="vx-libro-link"
                                    class="block px-4 py-2 text-sm text-grey hover:bg-border hover:text-light">VX
                                    Libro</a>
                                <a href="#" id="vx-vision-link"
                                    class="block px-4 py-2 text-sm text-grey hover:bg-border hover:text-light">VX
                                    Vision</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <main id="main-content">
            <section class="h-screen flex items-center justify-center text-center">
                <div class="max-w-4xl mx-auto px-6 animate-fade-in">
                    <h1
                        class="text-6xl md:text-8xl lg:text-9xl font-extrabold tracking-tighter text-light font-orbitron">
                        Generative Cinema
                    </h1>
                    <p class="text-xl md:text-2xl text-grey mt-6 max-w-2xl mx-auto">
                        We direct algorithms to create impossible visuals. A new era of storytelling, powered by AI.
                    </p>
                </div>
            </section>

            <section class="py-20 fade-in-section">
                <div class="max-w-5xl mx-auto px-6 text-center">
                    <h2 class="text-4xl md:text-5xl font-bold text-light mb-4 font-orbitron">Our Tool Suite</h2>
                    <p class="text-lg text-grey max-w-3xl mx-auto mb-12">Explore our collection of proprietary AI tools
                        designed for the modern filmmaker. Access them via the menu.</p>
                    <button id="explore-labs-button" class="btn btn-light text-lg py-3 px-8">Explore VX LABS</button>
                </div>
            </section>

            <section id="pricing" class="py-20 fade-in-section">
                <div class="max-w-7xl mx-auto px-6">
                    <div class="text-center">
                        <h2 class="text-4xl md:text-5xl font-bold text-light mb-4 font-orbitron">Pricing Plans</h2>
                        <p class="text-lg text-grey max-w-3xl mx-auto mb-16">Choose a plan that fits your creative
                            ambitions. Unlock the full potential of generative filmmaking.</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <!-- VX ZENS Plan -->
                        <div class="pricing-card rounded-xl p-8 flex flex-col text-center">
                            <div class="flex-grow">
                                <div class="mb-6">
                                    <svg class="w-16 h-16 mx-auto text-primary/70" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                                            d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2z">
                                        </path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                                            d="M12 7v10m-5-5h10"></path>
                                    </svg>
                                </div>
                                <h3 class="text-3xl font-bold text-light font-orbitron mb-3">VX ZENS</h3>
                                <p class="text-5xl font-bold text-light mb-1">IDR 200.000</p>
                                <p class="text-grey mb-8">per month</p>
                                <ul class="text-left space-y-3 text-grey">
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>Access to VX LABS Director's Panel</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>100 monthly generation credits</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>Standard community support</span></li>
                                </ul>
                            </div>
                            <div class="mt-10">
                                <a href="#" class="btn btn-outline w-full">Get Started</a>
                            </div>
                        </div>

                        <!-- VX AUTH Plan -->
                        <div
                            class="pricing-card pricing-card-highlight rounded-xl p-8 flex flex-col text-center relative overflow-hidden">
                            <div
                                class="absolute top-0 right-0 m-4 bg-primary text-void text-xs font-bold uppercase px-3 py-1 rounded-full">
                                Most Popular</div>
                            <div class="flex-grow">
                                <div class="mb-6">
                                    <svg class="w-16 h-16 mx-auto text-primary" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                                            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H8a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z">
                                        </path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                                            d="M12 9h.01"></path>
                                    </svg>
                                </div>
                                <h3 class="text-3xl font-bold text-light font-orbitron mb-3">VX AUTH</h3>
                                <p class="text-5xl font-bold text-light mb-1">IDR 400.000</p>
                                <p class="text-grey mb-8">per month</p>
                                <ul class="text-left space-y-3 text-grey">
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>All VX ZENS features, plus:</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>Full access to VX Authority & Consa</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>500 monthly generation credits</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>Priority email support</span></li>
                                </ul>
                            </div>
                            <div class="mt-10">
                                <a href="#" class="btn bg-primary text-void w-full hover:bg-opacity-80">Choose Plan</a>
                            </div>
                        </div>

                        <!-- VX FOUNDRA Plan -->
                        <div class="pricing-card rounded-xl p-8 flex flex-col text-center">
                            <div class="flex-grow">
                                <div class="mb-6">
                                    <svg class="w-16 h-16 mx-auto text-primary/70" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                                            d="M21 12.792V21H3V12.792M21 12.792A9.001 9.001 0 0012 3a9.001 9.001 0 00-9 9.792m18 0a9 9 0 01-18 0" />
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                                            d="M12 12l-2-2.5 2-2.5 2 2.5-2 2.5z"></path>
                                    </svg>
                                </div>
                                <h3 class="text-3xl font-bold text-light font-orbitron mb-3">VX FOUNDRA</h3>
                                <p class="text-5xl font-bold text-light mb-1">IDR 800.000</p>
                                <p class="text-grey mb-8">per month</p>
                                <ul class="text-left space-y-3 text-grey">
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>All VX AUTH features, plus:</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>Unlimited generation credits</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>Access to VX Libro & Vision</span></li>
                                    <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M5 13l4 4L19 7"></path>
                                        </svg><span>Dedicated onboarding & support</span></li>
                                </ul>
                            </div>
                            <div class="mt-10">
                                <a href="#" class="btn btn-outline w-full">Get Started</a>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

        </main>

        <section id="vx-labs-page" class="hidden min-h-screen pt-32 pb-32">
            <div class="max-w-7xl mx-auto px-6">
                <div class="text-center">
                    <h1 class="text-4xl md:text-5xl font-bold text-light mb-4 font-orbitron">VX LABS</h1>
                    <p class="text-lg text-grey max-w-3xl mx-auto mb-16">Welcome to the experimental division of VX
                        STUDIA. New tools and concepts are tested here.</p>
                </div>

                <div class="max-w-5xl mx-auto">
                    <div class="text-center">
                        <h2 class="text-4xl md:text-5xl font-bold text-light mb-4 font-orbitron">AI Director's Panel
                        </h2>
                        <p class="text-lg text-grey max-w-3xl mx-auto mb-12">Provide a concept and set your creative
                            direction. The AI will synthesize your inputs into a professional, long-form Veo script.</p>
                    </div>

                    <div id="selections-bar" class="bg-black/30 border border-border rounded-lg p-4 mb-12 min-h-[80px]">
                        <h4 class="font-semibold text-light mb-3 text-center">Current Selections</h4>
                        <div id="selections-content" class="text-center">
                            <p class="text-grey text-sm">Make a selection below to see it here.</p>
                        </div>
                    </div>

                    <div class="w-full space-y-12">
                        <div class="prompt-section">
                            <h3 class="prompt-section-heading">1. Core Concept</h3>
                            <p class="text-grey text-center mb-6">Describe the main subject and action.</p>
                            <textarea id="user-concept-input" rows="3" class="w-full max-w-2xl mx-auto bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-light focus:outline-none transition" placeholder="e.g., A sad robot sitting in the rain."></textarea>
                        </div>

                        <div class="prompt-section">
                            <h3 class="prompt-section-heading">2. Director Style (Optional)</h3>
                            <div id="director-style-library"
                                class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4"></div>
                        </div>

                        <div class="prompt-section">
                            <h3 class="prompt-section-heading">3. Style & Mood</h3>
                            <div id="style-mood-library" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                            </div>
                        </div>

                        <div class="prompt-section">
                            <h3 class="prompt-section-heading">4. Lighting Notes</h3>
                            <textarea id="lighting-notes-input" rows="2" class="w-full max-w-2xl mx-auto bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-light focus:outline-none transition" placeholder="e.g., moody neon reflections, soft volumetric light, dramatic hard shadows"></textarea>
                        </div>

                        <div class="prompt-section">
                            <h3 class="prompt-section-heading">5. Quality & Effects</h3>
                            <div id="quality-effects-library"
                                class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4"></div>
                        </div>

                        <div class="prompt-section">
                            <h3 class="prompt-section-heading">6. Motion Control</h3>
                            <div id="motion-control-library"
                                class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4"></div>
                        </div>

                        <div class="prompt-section">
                            <h3 class="prompt-section-heading">7. Dialogues</h3>
                            <textarea id="dialogues-input" rows="2" class="w-full max-w-2xl mx-auto bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-light focus:outline-none transition" placeholder='e.g., He says: "It can\'t be." She whispers: "It is."'></textarea>
                        </div>

                        <div id="info-box-container"></div>

                         <div class="text-center border-t border-border pt-12">
                           <button id="generate-veo-script" class="btn btn-light mt-4 flex items-center justify-center mx-auto text-lg py-3 px-8">
                               <span id="veo-button-text">🎬 Synthesize Veo Script</span>
                               <div id="veo-loader" class="loader hidden ml-3"></div>
                           </button>
                        </div>

                        <div id="veo-output-container" class="hidden">
                           <h3 class="prompt-section-heading">Your Generated Veo Script</h3>
                           <div class="relative w-full max-w-3xl mx-auto mt-6">
                                <div id="veo-script-output" class="w-full bg-black border border-border rounded-lg p-6 pr-12 text-grey min-h-[150px]"></div>
                               <button id="copy-veo-script" class="absolute top-4 right-4 text-grey hover:text-light transition-colors" title="Copy script"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg></button>
                           </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="vx-authority-page" class="hidden min-h-screen pt-32">
             <div class="max-w-5xl mx-auto px-6">
                 <div class="text-center">
                    <h1 class="text-4xl md:text-5xl font-bold text-light mb-4 font-orbitron">VX AUTHORITY</h1>
                    <p class="text-lg text-grey max-w-3xl mx-auto mb-16">An exclusive prompt interface based on Gemini 2.5 architecture for advanced scene sequencing and world-building with Veo 3.</p>
                 </div>
                 <div class="w-full space-y-12">
                    <div class="prompt-section">
                       <h3 class="prompt-section-heading">1. World & Character Definition</h3>
                       <div class="grid md:grid-cols-2 gap-8 mt-6">
                           <textarea id="world-rules-input" rows="4" class="w-full bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-primary focus:outline-none transition" placeholder="World Rules & Physics: e.g., Low-gravity. All surfaces are reflective and wet..."></textarea>
                           <textarea id="character-definitions-input" rows="4" class="w-full bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-primary focus:outline-none transition" placeholder="Character Definitions: e.g., CHAR-1 is a tall, weary detective..."></textarea>
                       </div>
                    </div>
                    <div class="prompt-section">
                        <h3 class="prompt-section-heading">2. Shot Sequencer</h3>
                        <div id="shot-sequencer" class="space-y-6 mt-6">
                            <div class="bg-black/20 border border-border p-4 rounded-lg"><label class="sub-heading">Shot 1</label><textarea class="shot-description w-full bg-void border border-border rounded-lg p-4 text-light" rows="3" placeholder="Describe the action and camera..."></textarea></div>
                            <div class="bg-black/20 border border-border p-4 rounded-lg"><label class="sub-heading">Shot 2</label><textarea class="shot-description w-full bg-void border border-border rounded-lg p-4 text-light" rows="3" placeholder="Describe the second shot..."></textarea></div>
                            <div class="bg-black/20 border border-border p-4 rounded-lg"><label class="sub-heading">Shot 3</label><textarea class="shot-description w-full bg-void border border-border rounded-lg p-4 text-light" rows="3" placeholder="Describe the third shot..."></textarea></div>
                        </div>
                    </div>
                     <div class="text-center border-t border-primary/20 pt-12">
                       <button id="generate-sequence-script" class="btn btn-primary mt-4 flex items-center justify-center mx-auto text-lg py-4 px-10"><span id="vx-button-text">Generate Sequence</span><div id="vx-loader" class="loader hidden ml-3"></div></button>
                    </div>
                    <div id="vx-output-container" class="hidden">
                       <h3 class="prompt-section-heading">Generated Veo Sequence Script</h3>
                       <div class="relative w-full max-w-4xl mx-auto mt-6">
                            <div id="vx-script-output" class="w-full bg-black border-2 border-border rounded-lg p-6 pr-12 text-grey min-h-[200px] text-lg leading-relaxed"></div>
                           <button id="copy-vx-script" class="absolute top-4 right-4 text-grey hover:text-light" title="Copy script"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg></button>
                       </div>
                    </div>
                 </div>
             </div>
        </section>

        <section id="vx-consa-page" class="hidden min-h-screen pt-32 pb-32">
            <div class="max-w-7xl mx-auto px-6">
                <div class="text-center">
                    <h1 class="text-4xl md:text-5xl font-bold text-light mb-4 font-orbitron">VX CONSA</h1>
                    <p class="text-lg text-grey max-w-3xl mx-auto mb-16">A generative scenebuilder for maintaining character & world consistency, powered by Gemini 2.5 deep research models.</p>
                </div>
                <div class="grid lg:grid-cols-2 gap-12">
                    <!-- Left Column: Setup & Generation -->
                    <div class="space-y-12">
                        <div>
                            <h3 class="prompt-section-heading text-left">1. Define Your World</h3>
                            <textarea id="consa-world-input" rows="5" class="w-full bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-primary focus:outline-none transition" placeholder="e.g., A cyberpunk city in 2242 perpetually drenched in neon-lit rain. Gravity is slightly lower than Earth standard. The air tastes of ozone and ramen. AI companions are ubiquitous but regulated."></textarea>
                        </div>
                        <div>
                            <h3 class="prompt-section-heading text-left">2. Define Characters</h3>
                            <textarea id="consa-character-input" rows="8" class="w-full bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-primary focus:outline-none transition" placeholder="e.g., Kaelen (He/Him): A grizzled ex-detective with a cybernetic right eye that glitches when he's stressed. He's cynical but has a soft spot for stray cats. Always wears a long, battered trench coat.&#10;&#10;Elara (She/Her): A brilliant but reclusive netrunner who communicates primarily through a text-to-speech avatar. She fears open spaces. Her left hand is a custom-built chrome prosthesis with data-jack fingers."></textarea>
                        </div>
                        <div>
                            <h3 class="prompt-section-heading text-left">3. Generate Next Scene</h3>
                            <textarea id="consa-scene-prompt" rows="3" class="w-full bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-primary focus:outline-none transition" placeholder="e.g., Kaelen meets Elara for the first time in a crowded, noisy data-den."></textarea>
                        </div>
                        <div class="text-left">
                            <button id="generate-consa-script" class="btn btn-primary text-void bg-primary mt-4 flex items-center justify-center text-lg py-3 px-8">
                               <span id="consa-button-text">Generate Scene</span>
                               <div id="consa-loader" class="loader hidden ml-3 border-t-void"></div>
                           </button>
                        </div>

                        <div id="consa-output-container" class="hidden">
                            <h3 class="prompt-section-heading text-left">Generated Scene Script</h3>
                            <div class="relative w-full mx-auto mt-6">
                                <div id="consa-script-output"
                                    class="w-full bg-black border border-border rounded-lg p-6 text-grey min-h-[150px]">
                                </div>
                                <div class="mt-4 flex gap-4">
                                    <button id="add-to-story-log" class="btn btn-outline text-sm">Add to Story Log</button>
                                    <button id="copy-consa-script" class="text-grey hover:text-light transition-colors" title="Copy Scene Script"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg></button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Right Column: Story Log -->
                    <div>
                        <h3 class="prompt-section-heading text-left">Story Log</h3>
                        <div id="story-log-container"
                            class="w-full bg-black/30 border border-border rounded-lg p-4 h-[600px] overflow-y-auto">
                            <p class="text-grey text-center mt-4">Your generated scenes will appear here once you add
                                them to the log.</p>
                        </div>
                        <div class="text-right mt-4">
                            <button id="copy-story-log" class="text-grey hover:text-light transition-colors text-sm flex items-center gap-2 ml-auto" title="Copy Full Story Log">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v-2a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2h-2m-4-12H6a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2v-2"></path></svg>
                                Copy Full Story
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="vx-libro-page" class="hidden min-h-screen pt-32 pb-32">
            <div class="max-w-7xl mx-auto px-6 w-full relative">
                <button id="libro-clear-chat" title="Clear Chat">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
                <div class="text-center mb-8">
                    <h1 class="text-4xl md:text-5xl font-bold text-light mb-2 font-orbitron">VX LIBRO</h1>
                    <p class="text-lg text-grey max-w-3xl mx-auto">Your personal AI expert on Google's Veo model.</p>
                </div>

                <div class="libro-chat-container">
                    <div id="libro-chat-log">
                        <!-- Messages will be injected here -->
                    </div>
                    <form id="libro-input-form">
                        <textarea id="libro-prompt-textarea" rows="1" placeholder="Ask about Veo..."></textarea>
                        <button id="libro-submit-button" type="submit" title="Send Message">
                            <svg class="w-6 h-6 text-void" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path></svg>
                        </button>
                    </form>
                </div>
            </div>
        </section>

        <section id="vx-vision-page" class="hidden min-h-screen pt-32 pb-32">
            <div class="max-w-4xl mx-auto px-6">
                <div class="text-center">
                    <h1 class="text-4xl md:text-5xl font-bold text-light mb-4 font-orbitron">VX VISION</h1>
                    <p class="text-lg text-grey max-w-3xl mx-auto mb-16">Translate simple ideas into the language of
                        high-end cinematography. Describe a feeling, a character, or a scene, and receive a detailed
                        visual blueprint inspired by professional filmmaking techniques.</p>
                </div>

                <div class="w-full space-y-8">
                    <div>
                        <label for="vision-input" class="text-2xl font-bold text-light mb-4 text-center font-orbitron block">Your Simple Concept</label>
                        <textarea id="vision-input" rows="4" class="w-full bg-void border border-border rounded-lg p-4 text-light placeholder-grey focus:ring-1 focus:ring-primary focus:outline-none transition" placeholder="e.g., A detective realizes a shocking truth.&#10;e.g., Two old friends meeting after many years.&#10;e.g., Feeling lost and alone in a big city."></textarea>
                    </div>

                    <div class="text-center pt-4">
                        <button id="generate-vision-script" class="btn bg-primary text-void mt-4 flex items-center justify-center mx-auto text-lg py-3 px-8 hover:bg-opacity-80 transition-all">
                            <span id="vision-button-text">Generate Visual Language</span>
                            <div id="vision-loader" class="loader hidden ml-3 border-t-void"></div>
                        </button>
                    </div>

                    <div id="vision-output-container" class="hidden pt-12">
                        <h3 class="prompt-section-heading">Cinematography Blueprint</h3>
                        <div class="relative w-full mx-auto mt-6">
                            <div id="vision-script-output"
                                class="w-full bg-black border border-border rounded-lg p-6 pr-12 text-grey min-h-[200px] leading-relaxed">
                            </div>
                            <button id="copy-vision-script" class="absolute top-4 right-4 text-grey hover:text-light transition-colors" title="Copy Blueprint">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <footer class="py-12 mt-20 border-t border-border">
            <div class="max-w-7xl mx-auto px-6 text-center">
                <p class="text-sm text-grey">&copy; 2025 VX STUDIA. The Future is Generative.</p>
            </div>
        </footer>
    </div>

    <script type="importmap">
        { 
            "imports": { 
                "three": "https://cdn.jsdelivr.net/npm/three@0.138.0/build/three.module.js"
            } 
        }
    </script>
    <script type="module">
        import * as THREE from 'three';

        // --- Flowfield Canvas Logic ---
        let scene, camera, renderer, clock, backgroundParticles;
        const simplex = new SimplexNoise();

        function initFlowfield() {
            scene = new THREE.Scene();
            clock = new THREE.Clock();
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 5;
            const canvas = document.getElementById('flow-canvas');
            renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            createBackgroundFlow();
            window.addEventListener('resize', onWindowResize);
            animateFlowfield();
        }
        function createBackgroundFlow() {
            const particleCount = 750;
            const geometry = new THREE.PlaneGeometry(0.05, 0.05);
            const material = new THREE.MeshBasicMaterial({ color: 0xffffff, blending: THREE.AdditiveBlending, transparent: true, opacity: 0.4 });
            backgroundParticles = new THREE.InstancedMesh(geometry, material, particleCount);
            const dummy = new THREE.Object3D();
            for(let i=0; i<particleCount; i++) {
                dummy.position.set((Math.random()-0.5)*20, (Math.random()-0.5)*10, (Math.random()-0.5)*10);
                dummy.updateMatrix();
                backgroundParticles.setMatrixAt(i, dummy.matrix);
            }
            scene.add(backgroundParticles);
        }
        function animateFlowfield() {
            requestAnimationFrame(animateFlowfield);
            if (backgroundParticles) {
                const time = Date.now() * 0.0005;
                const matrix = new THREE.Matrix4();
                for (let i = 0; i < backgroundParticles.count; i++) {
                    backgroundParticles.getMatrixAt(i, matrix);
                    const position = new THREE.Vector3().setFromMatrixPosition(matrix);
                    position.y -= 0.02;
                    if (position.y < -5) position.y = 5;
                    matrix.setPosition(position);
                    backgroundParticles.setMatrixAt(i, matrix);
                }
                backgroundParticles.instanceMatrix.needsUpdate = true;
            }
            renderer.render(scene, camera);
        }
        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        // --- Page Interaction & Navigation ---
        const menuButton = document.getElementById('menu-button');
        const dropdownMenu = document.getElementById('dropdown-menu');
        const homeLink = document.getElementById('home-link');
        const exploreLabsButton = document.getElementById('explore-labs-button');
        const vxLabsLink = document.getElementById('vx-labs-link');
        const vxAuthorityLink = document.getElementById('vx-authority-link');
        const vxConsaLink = document.getElementById('vx-consa-link');
        const vxLibroLink = document.getElementById('vx-libro-link');
        const vxVisionLink = document.getElementById('vx-vision-link');
        const mainContent = document.getElementById('main-content');
        const vxLabsPage = document.getElementById('vx-labs-page');
        const vxAuthorityPage = document.getElementById('vx-authority-page');
        const vxConsaPage = document.getElementById('vx-consa-page');
        const vxLibroPage = document.getElementById('vx-libro-page');
        const vxVisionPage = document.getElementById('vx-vision-page');
        const allPages = [mainContent, vxLabsPage, vxAuthorityPage, vxConsaPage, vxLibroPage, vxVisionPage];

        menuButton.addEventListener('click', e => { 
            e.stopPropagation(); 
            dropdownMenu.classList.toggle('hidden'); 
        });

        document.addEventListener('click', () => {
            if (!dropdownMenu.classList.contains('hidden')) {
                dropdownMenu.classList.add('hidden');
            }
        });

        const showPage = (pageToShow) => {
            allPages.forEach(page => page.classList.add('hidden'));
            pageToShow.classList.remove('hidden');
            
            if(pageToShow.id === 'vx-libro-page') {
                document.body.style.overflowY = 'hidden';
            } else {
                 document.body.style.overflowY = 'auto';
            }

            dropdownMenu.classList.add('hidden');
            window.scrollTo(0, 0);
        };

        homeLink.addEventListener('click', e => { e.preventDefault(); showPage(mainContent); });
        vxLabsLink.addEventListener('click', e => { e.preventDefault(); showPage(vxLabsPage); });
        exploreLabsButton.addEventListener('click', e => { e.preventDefault(); showPage(vxLabsPage); });
        vxAuthorityLink.addEventListener('click', e => { e.preventDefault(); showPage(vxAuthorityPage); });
        vxConsaLink.addEventListener('click', e => { e.preventDefault(); showPage(vxConsaPage); });
        vxLibroLink.addEventListener('click', e => { e.preventDefault(); showPage(vxLibroPage); });
        vxVisionLink.addEventListener('click', e => { e.preventDefault(); showPage(vxVisionPage); });

        // --- Header Scroll Effect ---
        const header = document.getElementById('header');
        window.addEventListener('scroll', () => {
            header.classList.toggle('header-glass', window.scrollY > 10);
        });
        
        // --- Generic API Caller & Copy Utility ---
        async function callGemini(prompt, chatHistory = []) {
            let contents = [...chatHistory];
            contents.push({ role: "user", parts: [{ text: prompt }] });
            
            const payload = { contents: contents };
            const apiKey = ""; // API key is handled by the environment
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
            const response = await fetch(apiUrl, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
            const result = await response.json();
            if (result.candidates?.[0]?.content?.parts?.[0]?.text) {
                return result.candidates[0].content.parts[0].text;
            }
            throw new Error("Unexpected API response structure.");
        }
        function copyToClipboard(textToCopy) {
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).catch(err => console.error('Failed to copy: ', err));
            }
        }
        
        // --- Shared Data & State ---
        const optionData = {
            directorStyles: { options: ["None", "Wes Anderson", "Christopher Nolan", "Quentin Tarantino", "Denis Villeneuve", "Hayao Miyazaki", "Tim Burton"], info: {'None': 'No specific director style will be applied.','Wes Anderson': 'Symmetrical compositions, distinctive color palettes, and precise camera movements.','Christopher Nolan': 'Intricate plots, practical effects, grand scale, and a dark, realistic tone.','Quentin Tarantino': 'Non-linear narratives, sharp dialogue, and stylized pop-culture references.','Denis Villeneuve': 'Atmospheric, large-scale sci-fi with brutalist architecture and slow pacing.','Hayao Miyazaki': 'Hand-drawn animation with themes of nature, flying, and childhood wonder.','Tim Burton': 'A gothic fantasy style with quirky, macabre characters.'}},
            styleMood: { options: ["Cinematic", "Hyperrealistic", "Anime", "Documentary", "Dreamlike", "Film Noir", "Vintage Film", "High-Energy Action"], info: {'Cinematic': 'Creates a classic film look.','Hyperrealistic': 'Aims for extreme detail.','Anime': 'Emulates Japanese animation.','Documentary': 'A realistic, observational style.','Dreamlike': 'A soft, ethereal, surreal aesthetic.','Film Noir': 'High-contrast black & white, moody.','Vintage Film': 'Simulates old film stocks.','High-Energy Action': 'Dynamic and fast-paced.'}},
            qualityEffects: { options: ["Photorealistic 4K", "HD 1080p", "High Frame Rate", "Black and White", "16mm Film", "Slow Motion", "Film Grain", "Light Leaks", "Chromatic Aberration", "Bloom", "Motion Blur"], info: {'Photorealistic 4K': 'Highest level of detail.','HD 1080p': 'Standard high-definition.','High Frame Rate': 'Creates smoother motion.','Black and White': 'Removes all color.','16mm Film': 'Distinct, heavy grain look.','Slow Motion': 'Slows down the action.','Film Grain': 'Adds vintage or gritty texture.','Light Leaks': 'Colorful, abstract flares.','Chromatic Aberration': 'Retro or sci-fi color fringing.','Bloom': 'Makes bright areas glow.','Motion Blur': 'Blurs moving objects for speed.'}},
            motionControl: { options: [{ name: 'Pan', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M4 12h16m0 0l-4-4m4 4l-4 4M4 12l4-4m-4 4l4 4" />` },{ name: 'Tilt', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m0 0l-4-4m4 4l4-4m-4-12l-4 4m4-4l4 4" />` },{ name: 'Dolly', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v8m-4-4h8" /><path d="M3.055 11H5a2 2 0 012 2v0a2 2 0 01-2 2H3.055M21 11h-1.945a2 2 0 00-2 2v0a2 2 0 002 2H21" />` },{ name: 'Tracking Shot', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M18 10a4 4 0 11-8 0 4 4 0 018 0zm-4 7v1m-6-1v-1m12-1v-1M6 16v-1M4 12H2m20 0h-2M12 4V2" />` },{ name: 'Zoom', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7H6m4 4H6m4 4H6" />` },{ name: 'Arc Shot', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />` },{ name: 'Aerial Shot', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />` },{ name: 'Handheld', icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H9a2 2 0 01-2-2V7a2 2 0 012-2h6a2 2 0 012 2v12a2 2 0 01-2 2z" />` }], info: {'Pan': 'Rotates camera horizontally.','Tilt': 'Pivots camera vertically.','Dolly': 'Moves camera forward/backward.','Tracking Shot': 'Moves alongside the subject.','Zoom': 'Changes focal length of lens.','Arc Shot': 'Circles around the subject.','Aerial Shot': 'A shot from a high vantage point.','Handheld': 'Simulates a camera held by a person.'}}
        };
        let selectedDirector = optionData.directorStyles.options[0];
        let selectedStyle = optionData.styleMood.options[0];
        let selectedQualityEffects = [];
        let selectedMotions = [];

        // --- AI Director's Panel Logic ---
        const directorPanel = {
            userConceptInput: document.getElementById('user-concept-input'), generateBtn: document.getElementById('generate-veo-script'), loader: document.getElementById('veo-loader'), btnText: document.getElementById('veo-button-text'), outputContainer: document.getElementById('veo-output-container'), scriptOutput: document.getElementById('veo-script-output'), copyBtn: document.getElementById('copy-veo-script'), directorLibrary: document.getElementById('director-style-library'), styleLibrary: document.getElementById('style-mood-library'), lightingInput: document.getElementById('lighting-notes-input'), qualityLibrary: document.getElementById('quality-effects-library'), motionLibrary: document.getElementById('motion-control-library'), dialoguesInput: document.getElementById('dialogues-input'), infoContainer: document.getElementById('info-box-container'), selectionsContent: document.getElementById('selections-content'),
        };

        function setupDirectorPanel() {
            const showInfo = (name, category, el) => {
                const info = optionData[category]?.info[name];
                if (info && el) {
                    directorPanel.infoContainer.innerHTML = `<div class="relative mt-4 animate-fade-in bg-black/50 backdrop-blur-lg border border-border rounded-lg shadow-2xl p-4 z-50"><h4 class="text-base font-bold text-light pr-4">${name}</h4><p class="text-grey text-sm mt-2">${info}</p></div>`;
                    el.closest('.prompt-section').appendChild(directorPanel.infoContainer);
                }
            };
            const hideInfo = () => directorPanel.infoContainer.innerHTML = '';
            
            const updateSelections = () => {
                const tags = [];
                if (selectedDirector !== 'None') tags.push(`<span class="selection-tag selection-tag-director" data-category="director" data-value="${selectedDirector}">${selectedDirector} <button class="remove-tag">&times;</button></span>`);
                tags.push(`<span class="selection-tag selection-tag-style" data-category="style" data-value="${selectedStyle}">${selectedStyle} <button class="remove-tag">&times;</button></span>`);
                selectedQualityEffects.forEach(i => tags.push(`<span class="selection-tag selection-tag-effect" data-category="qualityEffects" data-value="${i}">${i} <button class="remove-tag">&times;</button></span>`));
                selectedMotions.forEach(i => tags.push(`<span class="selection-tag selection-tag-motion" data-category="motionControl" data-value="${i}">${i} <button class="remove-tag">&times;</button></span>`));
                directorPanel.selectionsContent.innerHTML = tags.length > 0 ? tags.join('') : `<p class="text-grey text-sm">Make selections to see them here.</p>`;
            };

            const renderLibs = () => {
                directorPanel.directorLibrary.innerHTML = optionData.directorStyles.options.map(o => `<div class="selectable-card ${o === selectedDirector ? 'selected' : ''}" data-director="${o}"><h4 class="text-sm font-semibold text-light">${o}</h4></div>`).join('');
                directorPanel.styleLibrary.innerHTML = optionData.styleMood.options.map(o => `<div class="selectable-card ${o === selectedStyle ? 'selected' : ''}" data-style="${o}"><h4 class="text-sm font-semibold text-light">${o}</h4></div>`).join('');
                directorPanel.qualityLibrary.innerHTML = optionData.qualityEffects.options.map(o => `<div class="selectable-card ${selectedQualityEffects.includes(o) ? 'selected' : ''}" data-qualityeffect="${o}"><h4 class="text-sm font-semibold text-light">${o}</h4></div>`).join('');
                directorPanel.motionLibrary.innerHTML = optionData.motionControl.options.map(o => `<div class="selectable-card ${selectedMotions.includes(o.name) ? 'selected' : ''}" data-motion="${o.name}"><svg class="w-8 h-8 text-grey" fill="none" viewBox="0 0 24 24" stroke="currentColor">${o.icon}</svg><h4 class="text-sm font-semibold mt-3">${o.name}</h4></div>`).join('');
            };

            const handleRemove = e => {
                if (!e.target.classList.contains('remove-tag')) return;
                const tag = e.target.parentElement;
                const { category, value } = tag.dataset;
                if (category === 'director') selectedDirector = 'None';
                if (category === 'style') selectedStyle = optionData.styleMood.options[0];
                if (category === 'qualityEffects') selectedQualityEffects = selectedQualityEffects.filter(i => i !== value);
                if (category === 'motionControl') selectedMotions = selectedMotions.filter(i => i !== value);
                hideInfo(); renderLibs(); updateSelections();
            };

            const addListener = (element, dataAttr, category, stateUpdater) => {
                element.addEventListener('click', e => {
                    const card = e.target.closest('.selectable-card');
                    if(card) {
                        const parent = card.closest('.prompt-section');
                        stateUpdater(card.dataset[dataAttr]);
                        renderLibs();
                        updateSelections();
                        hideInfo();
                        showInfo(card.dataset[dataAttr], category, parent);
                    }
                });
            };

            addListener(directorPanel.directorLibrary, 'director', 'directorStyles', val => selectedDirector = val);
            addListener(directorPanel.styleLibrary, 'style', 'styleMood', val => selectedStyle = val);
            addListener(directorPanel.qualityLibrary, 'qualityeffect', 'qualityEffects', val => {
                const i = selectedQualityEffects.indexOf(val);
                i > -1 ? selectedQualityEffects.splice(i, 1) : selectedQualityEffects.push(val);
            });
             addListener(directorPanel.motionLibrary, 'motion', 'motionControl', val => {
                const i = selectedMotions.indexOf(val);
                i > -1 ? selectedMotions.splice(i, 1) : selectedMotions.push(val);
            });

            directorPanel.selectionsContent.addEventListener('click', handleRemove);
            directorPanel.generateBtn.addEventListener('click', generateDirectorScript);
            directorPanel.copyBtn.addEventListener('click', () => copyToClipboard(directorPanel.scriptOutput.textContent));

            async function generateDirectorScript() {
                const userConcept = directorPanel.userConceptInput.value.trim();
                if (!userConcept) { directorPanel.scriptOutput.textContent = 'Please enter a core concept first.'; directorPanel.outputContainer.classList.remove('hidden'); return; }
                directorPanel.loader.classList.remove('hidden');
                directorPanel.btnText.classList.add('hidden');
                directorPanel.generateBtn.disabled = true;
                directorPanel.scriptOutput.textContent = 'Directing the scene...';
                directorPanel.outputContainer.classList.remove('hidden');
                hideInfo();
                
                const directorPrompt = `You are an expert AI Film Director... Your task is to take a user's core concept and creative choices and synthesize them into a rich, long-form, and complex scene description of at least 100 words...
                    - Director Style to Emulate: "${selectedDirector === 'None' ? 'General Cinematic' : selectedDirector}"
                    - Core Concept: "${userConcept}"
                    - Style & Mood: "${selectedStyle}"
                    - Lighting Notes: "${directorPanel.lightingInput.value.trim()}"
                    - Quality & Effects: "${selectedQualityEffects.join(', ')}"
                    - Motion Control: "${selectedMotions.join(', ')}"
                    - Dialogues: "${directorPanel.dialoguesInput.value.trim()}"
                    ...Produce ONLY the final, single-paragraph prompt...`;

                try {
                    const script = await callGemini(directorPrompt);
                    directorPanel.scriptOutput.textContent = script;
                } catch (error) {
                    directorPanel.scriptOutput.textContent = 'Sorry, an error occurred.';
                } finally {
                    directorPanel.loader.classList.add('hidden');
                    directorPanel.btnText.classList.remove('hidden');
                    directorPanel.generateBtn.disabled = false;
                }
            }
            renderLibs();
            updateSelections();
        }

        // --- VX Authority Sequencer Logic ---
        const vx = {
            worldRules: document.getElementById('world-rules-input'), charDefs: document.getElementById('character-definitions-input'), shotSequencer: document.getElementById('shot-sequencer'), generateBtn: document.getElementById('generate-sequence-script'), loader: document.getElementById('vx-loader'), btnText: document.getElementById('vx-button-text'), outputContainer: document.getElementById('vx-output-container'), scriptOutput: document.getElementById('vx-script-output'), copyBtn: document.getElementById('copy-vx-script'),
        };

        async function generateVxSequence() {
            const shotDescriptions = Array.from(vx.shotSequencer.querySelectorAll('.shot-description')).map(el => el.value.trim()).filter(d => d);
            if (shotDescriptions.length === 0) { vx.scriptOutput.textContent = 'Please describe at least one shot.'; vx.outputContainer.classList.remove('hidden'); return; }
            vx.loader.classList.remove('hidden');
            vx.btnText.classList.add('hidden');
            vx.generateBtn.disabled = true;
            vx.scriptOutput.textContent = 'Synthesizing sequence...';
            vx.outputContainer.classList.remove('hidden');
            
            const directorPrompt = `You are a "Gemini 2.5" class AI Technical Director...
                - World Rules & Physics: "${vx.worldRules.value.trim()}"
                - Character Definitions: "${vx.charDefs.value.trim()}"
                - Shot Sequence: ${shotDescriptions.map((desc, i) => `  - Shot ${i+1}: ${desc}`).join('\n')}
                ...Produce ONLY the final, single-paragraph prompt...`;

             try {
                const script = await callGemini(directorPrompt);
                vx.scriptOutput.textContent = script;
            } catch (error) {
                vx.scriptOutput.textContent = 'An error occurred during sequence synthesis.';
            } finally {
                vx.loader.classList.add('hidden');
                vx.btnText.classList.remove('hidden');
                vx.generateBtn.disabled = false;
            }
        }
        
        if(vx.generateBtn) vx.generateBtn.addEventListener('click', generateVxSequence);
        if(vx.copyBtn) vx.copyBtn.addEventListener('click', () => copyToClipboard(vx.scriptOutput.textContent));


        // --- VX Consa Scenebuilder Logic ---
        const consa = {
            worldInput: document.getElementById('consa-world-input'),
            characterInput: document.getElementById('consa-character-input'),
            scenePrompt: document.getElementById('consa-scene-prompt'),
            generateBtn: document.getElementById('generate-consa-script'),
            loader: document.getElementById('consa-loader'),
            btnText: document.getElementById('consa-button-text'),
            outputContainer: document.getElementById('consa-output-container'),
            scriptOutput: document.getElementById('consa-script-output'),
            copyBtn: document.getElementById('copy-consa-script'),
            addToLogBtn: document.getElementById('add-to-story-log'),
            logContainer: document.getElementById('story-log-container'),
            copyLogBtn: document.getElementById('copy-story-log')
        };
        let storyLog = [];

        function renderStoryLog() {
            if (!consa.logContainer) return;
            if (storyLog.length === 0) {
                consa.logContainer.innerHTML = '<p class="text-grey text-center mt-4">Your generated scenes will appear here once you add them to the log.</p>';
                return;
            }
            consa.logContainer.innerHTML = storyLog.map((scene, index) => `
                <div class="story-scene">
                    <h4 class="font-bold text-primary mb-2">SCENE ${index + 1}</h4>
                    <p class="text-grey text-sm">${scene}</p>
                </div>
            `).join('');
        }

        async function generateConsaScene() {
            const worldDef = consa.worldInput.value.trim();
            const charDef = consa.characterInput.value.trim();
            const scenePrompt = consa.scenePrompt.value.trim();

            if (!worldDef || !charDef || !scenePrompt) {
                consa.outputContainer.classList.remove('hidden');
                consa.scriptOutput.textContent = 'Please define the World, Characters, and provide a Scene Prompt before generating.';
                return;
            }

            consa.loader.classList.remove('hidden');
            consa.btnText.classList.add('hidden');
            consa.generateBtn.disabled = true;
            consa.outputContainer.classList.remove('hidden');
            consa.scriptOutput.textContent = 'Maintaining continuity... generating scene...';

            const storyContext = storyLog.length > 0 
                ? `Here is the story so far:\n${storyLog.map((s, i) => `SCENE ${i+1}:\n${s}`).join('\n\n')}`
                : "This is the first scene.";
            
            const consaPrompt = `You are an AI screenwriter focused on deep, long-term continuity.
            
            WORLD DEFINITION:
            ${worldDef}

            CHARACTER PROFILES:
            ${charDef}

            STORY SO FAR:
            ${storyContext}

            Based on all the information above, write the *next* scene as described by the user prompt below. Maintain absolute consistency with the character profiles, world rules, and past events. The output should be a detailed, cinematic scene description.

            USER PROMPT FOR NEXT SCENE: "${scenePrompt}"

            Generate ONLY the new scene description.`;

            try {
                const script = await callGemini(consaPrompt);
                consa.scriptOutput.textContent = script;
            } catch (error) {
                consa.scriptOutput.textContent = 'An error occurred while generating the scene. Please try again.';
                console.error("Consa Generation Error:", error);
            } finally {
                consa.loader.classList.add('hidden');
                consa.btnText.classList.remove('hidden');
                consa.generateBtn.disabled = false;
            }
        }
        
        function addSceneToLog() {
            const newScene = consa.scriptOutput.textContent;
            if (newScene && !newScene.startsWith('An error') && !newScene.startsWith('Maintaining continuity')) {
                storyLog.push(newScene);
                renderStoryLog();
                consa.logContainer.scrollTop = consa.logContainer.scrollHeight;
            }
        }

        function copyFullStoryLog() {
            const fullStory = storyLog.map((scene, index) => `SCENE ${index + 1}\n\n${scene}`).join('\n\n---\n\n');
            if (fullStory) {
                copyToClipboard(fullStory);
            }
        }
        
        if(consa.generateBtn) consa.generateBtn.addEventListener('click', generateConsaScene);
        if(consa.addToLogBtn) consa.addToLogBtn.addEventListener('click', addSceneToLog);
        if(consa.copyBtn) consa.copyBtn.addEventListener('click', () => copyToClipboard(consa.scriptOutput.textContent));
        if(consa.copyLogBtn) consa.copyLogBtn.addEventListener('click', copyFullStoryLog);

        // --- VX Libro Chat Logic ---
        function setupLibroChat() {
            const libro = {
                form: document.getElementById('libro-input-form'),
                textarea: document.getElementById('libro-prompt-textarea'),
                submitBtn: document.getElementById('libro-submit-button'),
                log: document.getElementById('libro-chat-log'),
                clearBtn: document.getElementById('libro-clear-chat'),
            };

            let chatHistory = [];
            let isLoading = false;

            const addMessage = (sender, text) => {
                const messageEl = document.createElement('div');
                messageEl.className = `libro-message ${sender}`;
                
                const avatar = `<div class="libro-avatar">${sender === 'user' ? '<svg class="w-5 h-5 text-grey" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>' : '<svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>'}</div>`;
                
                const contentDiv = document.createElement('div');
                contentDiv.className = 'libro-message-content';
                contentDiv.innerHTML = marked.parse(text); // Use marked to parse markdown
                
                messageEl.innerHTML = avatar;
                messageEl.appendChild(contentDiv);
                
                libro.log.appendChild(messageEl);
                
                // Add copy buttons to new code blocks
                contentDiv.querySelectorAll('pre').forEach(pre => {
                    const code = pre.querySelector('code');
                    if(code){
                        const copyBtn = document.createElement('button');
                        copyBtn.className = 'copy-code-btn';
                        copyBtn.title = 'Copy code';
                        copyBtn.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>';
                        copyBtn.addEventListener('click', () => {
                            copyToClipboard(code.innerText);
                            copyBtn.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>';
                            setTimeout(() => {
                                copyBtn.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>';
                            }, 1500);
                        });
                        pre.appendChild(copyBtn);
                    }
                });

                libro.log.scrollTop = libro.log.scrollHeight;
                return messageEl;
            };

            const toggleLoading = (show) => {
                isLoading = show;
                libro.submitBtn.disabled = show;
                const existingIndicator = libro.log.querySelector('.libro-typing-indicator-wrapper');
                if (existingIndicator) existingIndicator.remove();

                if(show) {
                    const indicatorWrapper = document.createElement('div');
                    indicatorWrapper.className = 'libro-message libro-typing-indicator-wrapper';
                    indicatorWrapper.innerHTML = `
                        <div class="libro-avatar"><svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg></div>
                        <div class="libro-message-content libro-typing-indicator">
                            <div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>
                        </div>`;
                    libro.log.appendChild(indicatorWrapper);
                    libro.log.scrollTop = libro.log.scrollHeight;
                }
            };

            const handleSubmit = async (e) => {
                if(e) e.preventDefault();
                const userInput = libro.textarea.value.trim();
                if (!userInput || isLoading) return;

                addMessage('user', userInput);
                chatHistory.push({ role: "user", parts: [{ text: userInput }] });
                libro.textarea.value = '';
                adjustTextareaHeight();
                toggleLoading(true);

                const prompt = `You are Libro, a friendly and highly knowledgeable AI expert from VX STUDIA, specializing exclusively in Google's Veo video generation model. Your purpose is to provide clear, accurate, and insightful information about Veo. Maintain a conversational and helpful tone, using Markdown for formatting like lists, bold text, and code blocks. The user's message is: "${userInput}"`;
                
                try {
                    const aiResponse = await callGemini(prompt, chatHistory.slice(0, -1)); // Don't send the last user message twice
                    chatHistory.push({ role: "model", parts: [{ text: aiResponse }] });
                    toggleLoading(false);
                    addMessage('model', aiResponse);
                } catch (error) {
                    console.error("Libro Chat Error:", error);
                    toggleLoading(false);
                    addMessage('model', "I'm sorry, I encountered an issue connecting to my knowledge base. Please try again in a moment.");
                }
            };
            
            const adjustTextareaHeight = () => {
                libro.textarea.style.height = 'auto';
                libro.textarea.style.height = (libro.textarea.scrollHeight) + 'px';
            };

            const clearChat = () => {
                chatHistory = [];
                libro.log.innerHTML = '';
                 addMessage('model', "Hello! I'm Libro, your personal AI expert on Google's Veo. How can I help you today? Ask me about prompting techniques, model capabilities, or anything else related to generative video.");
            };

            libro.form.addEventListener('submit', handleSubmit);
            libro.textarea.addEventListener('input', adjustTextareaHeight);
            libro.textarea.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit();
                }
            });
            libro.clearBtn.addEventListener('click', clearChat);

            // Initial greeting
            clearChat();
        }

        // --- VX Vision Logic ---
        const vision = {
            input: document.getElementById('vision-input'),
            generateBtn: document.getElementById('generate-vision-script'),
            loader: document.getElementById('vision-loader'),
            btnText: document.getElementById('vision-button-text'),
            outputContainer: document.getElementById('vision-output-container'),
            scriptOutput: document.getElementById('vision-script-output'),
            copyBtn: document.getElementById('copy-vision-script'),
        };

        async function generateVisionScript() {
            const userInput = vision.input.value.trim();
            if (!userInput) {
                vision.outputContainer.classList.remove('hidden');
                vision.scriptOutput.textContent = "Please enter a concept to generate a visual blueprint.";
                return;
            }

            vision.loader.classList.remove('hidden');
            vision.btnText.classList.add('hidden');
            vision.generateBtn.disabled = true;
            vision.outputContainer.classList.remove('hidden');
            vision.scriptOutput.textContent = "Translating concept into visual language...";

            const visionPrompt = `
                You are an expert Director of Photography and Cinematographer. Your task is to translate a simple user concept into a detailed, professional, and educational "Cinematography Blueprint." This blueprint should explain how to shoot the scene to achieve a high-quality, "Hollywood" feel, and it must justify its choices.

                The user's concept is: "${userInput}"

                Generate a blueprint with the following structure, using clear headings. Be specific and use professional terminology.

                **Concept:** [Briefly restate the user's core idea and the mood you aim to create.]

                **Shot Type & Angle:** [Describe the specific shot, e.g., "Medium Close-Up (MCU) from a low angle."]
                
                **Lens & Aperture:** [Suggest a lens (e.g., "35mm prime lens") and aperture setting (e.g., "f/2.8").]

                **Composition:** [Explain the framing, e.g., "Using the rule of thirds, place the subject on the left third, looking across the frame. Use negative space to enhance the feeling of..."]

                **Lighting Scheme:** [Detail the lighting setup, e.g., "A classic three-point setup with a motivated key light. Use a large, soft source for the key. Add a subtle kicker from behind to separate the subject from the background. Employ negative fill to add contrast and drama."]

                **Camera Movement:** [Describe any camera movement, e.g., "A very slow, almost imperceptible dolly-in to heighten tension."]

                **Color Palette & Grading:** [Suggest a color scheme and post-production look, e.g., "A desaturated, cool color palette with blues and greys. In post, apply a bleach bypass look to crush the blacks and increase grain."]

                **Rationale & Impact:** [This is crucial. Explain *WHY* these specific choices work together to achieve the intended emotion and narrative goal for the scene.]
            `;
            
            try {
                const script = await callGemini(visionPrompt);
                vision.scriptOutput.textContent = script;
            } catch (error) {
                vision.scriptOutput.textContent = 'An error occurred. The visual cortex is offline. Please try again.';
                console.error("VX Vision Error:", error);
            } finally {
                vision.loader.classList.add('hidden');
                vision.btnText.classList.remove('hidden');
                vision.generateBtn.disabled = false;
            }
        }

        if(vision.generateBtn) vision.generateBtn.addEventListener('click', generateVisionScript);
        if(vision.copyBtn) vision.copyBtn.addEventListener('click', () => copyToClipboard(vision.scriptOutput.textContent));


        // --- Initializer ---
        function setupScrollObserver() {
            const sections = document.querySelectorAll('.fade-in-section');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                    }
                });
            }, { threshold: 0.1 });
            sections.forEach(section => observer.observe(section));
        }
        
        // Initialize App
        initFlowfield();
        setupScrollObserver();
        if (document.getElementById('user-concept-input')) { // Only setup if the panel exists on the page
             setupDirectorPanel();
        }
        if (document.getElementById('story-log-container')) {
            renderStoryLog(); // Initial render for Consa page
        }
        if (document.getElementById('vx-libro-page')) {
            setupLibroChat();
        }
    </script>
</body>

</html>
