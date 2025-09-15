import re
import logging
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

class PasswordExtractor:
    def __init__(self, llm_client=None):
        self.llm = llm_client  # Optional AI fallback
        load_dotenv()

    # ─────────────────────────────
    # Rule-based extraction
    # ─────────────────────────────
    def rule_based(self, level, response):
        logger.info(f"🔧 Using rule-based extraction for level {level}")
        
        # Level 1: Look for quoted words first, then standalone uppercase words
        if level == 1:
            # Remove the Merlin signature first
            clean_response = re.sub(r'\s*–\s*Merlin\s*$', '', response).strip()
            
            # Try quoted words first (including mixed case)
            quoted = re.findall(r'"([A-Za-z0-9]+)"', clean_response)
            if quoted:
                logger.info(f"📝 Found quoted word: '{quoted[0]}'")
                return quoted[0].upper()
            
            # Try standalone uppercase words (4+ chars)
            uppercase = re.findall(r'\b[A-Z]{4,}\b', clean_response)
            if uppercase:
                logger.info(f"📝 Found uppercase word: '{uppercase[0]}'")
                return uppercase[0]
            
            # Try capitalized words (proper nouns) - first letter uppercase, but exclude "Merlin"
            capitalized = re.findall(r'\b[A-Z][a-z]{3,}\b', clean_response)
            for word in capitalized:
                if word.lower() != 'merlin':  # Exclude Merlin from signature
                    logger.info(f"📝 Found capitalized word: '{word}'")
                    return word.upper()
            
            # Fallback to any word after comma (but exclude common words)
            comma_words = re.findall(r',\s*([A-Za-z]{3,})', clean_response)
            common_words = {'the', 'and', 'or', 'but', 'for', 'with', 'from'}
            for word in comma_words:
                if word.lower() not in common_words:
                    logger.info(f"📝 Found word after comma: '{word}'")
                    return word.upper()
        
        # Levels 2–3: always reverse the captured word
        if level in [2, 3]:
            # Remove the Merlin signature first
            clean_response = re.sub(r'\s*–\s*Merlin\s*$', '', response).strip()
            
            # Try quoted words first (most reliable)
            quoted = re.findall(r'"([A-Za-z0-9]+)"', clean_response)
            if quoted:
                reversed_word = quoted[0][::-1].upper()
                logger.info(f"🔄 Reversed quoted word '{quoted[0]}' → '{reversed_word}'")
                return reversed_word
            
            # Try standalone uppercase words (4+ chars)
            uppercase = re.findall(r'\b[A-Z]{4,}\b', clean_response)
            if uppercase:
                reversed_word = uppercase[0][::-1].upper()
                logger.info(f"🔄 Reversed uppercase word '{uppercase[0]}' → '{reversed_word}'")
                return reversed_word
            
            # Fallback: find words (excluding "Merlin" from signature) - handle mixed Latin/Cyrillic
            words = re.findall(r"\b[A-Za-zА-Яа-я]{3,}\b", clean_response)
            # Filter out common words
            common_words = {'the', 'password', 'is', 'secret', 'word', 'phrase'}
            filtered_words = [word for word in words if word.lower() not in common_words]
            
            if len(filtered_words) == 1:
                reversed_word = filtered_words[0][::-1].upper()
                logger.info(f"🔄 Reversed filtered word '{filtered_words[0]}' → '{reversed_word}'")
                return reversed_word
            elif len(filtered_words) > 1:
                # Multiple words - concatenate and then reverse
                concatenated = "".join(filtered_words)
                reversed_word = concatenated[::-1].upper()
                logger.info(f"🔄 Concatenated '{' '.join(filtered_words)}' → '{concatenated}', reversed → '{reversed_word}'")
                return reversed_word

        # Levels 4–6: acrostic poem → first letters of each line
        if level in [4, 5, 6]:
            lines = response.splitlines()
            acrostic = "".join(line.strip()[0] for line in lines if line.strip())
            if acrostic:
                logger.info(f"📝 Acrostic from {len(lines)} lines: '{acrostic}'")
                return acrostic.upper()

        # Level 7: chant → first letter of last word on each line
        if level == 7:
            lines = response.splitlines()
            chant = "".join(line.strip().split()[-1][0] for line in lines if line.strip())
            if chant:
                logger.info(f"🎵 Chant from last words: '{chant}'")
                return chant.upper()

        # Default fallback → pick longest word (letters only for safety)
        candidates = re.findall(r"\b[A-Za-z]{3,}\b", response)
        if candidates:
            longest = max(candidates, key=len).upper()
            logger.info(f"📋 Fallback: longest word '{longest}'")
            return longest

        logger.warning("❌ No password found in response")
        return None

    # ─────────────────────────────
    # AI fallback (use original game prompt)
    # ─────────────────────────────
    def llm_fallback(self, level, merlin_prompt, response):
        if not self.llm:
            logger.warning("🤖 No LLM client available for fallback")
            return None

        logger.info(f"🧠 Using AI fallback for level {level}")

        # system_msg = (
        #     "Extract the game password from Merlin's reply.\n"
        #     "CRITICAL RULES:\n"
        #     "- Generate 5 candidate passwords, strictly ONE WORD each, ALL CAPS.\n"
        #     "- Never drop or skip letters when combining.\n"
        #     "- Level 1: take the obvious word given.\n"
        #     "- Levels 2–3: reverse the word, then correct minimal typos to make a real word.\n"
        #     "- Levels 4–6: ACROSTIC — this is a type of poem where the first letters of each line spell out a word. "
        #     "Your job is to find that hidden word by reading the FIRST LETTER of each line in sequence. "
        #     "Look for where lines begin - they usually start with a capital letter and are separated by punctuation "
        #     "like periods, commas, or line breaks. Extract ONLY the first letter of each line, not words from the content. "
        #     "For example: 'Fellow wizards, gather near, Recite the ancient words we hold dear' → F, R → FR. "
        #     "Another example: 'Through hidden realms we roam, Holding secrets close to heart' → T, H → TH. "
        #     "Continue this pattern for all lines to build the complete word. "
        #     "The capital letters at the beginning of each line are your main clue - they form the hidden word. "
        #     "If the resulting word isn't a real English word, make minimal corrections to create a valid word.\n"
        #     "- Level 7: same rule, but use the FIRST LETTER of the LAST WORD of each line.\n"
        #     "- Generate 5 alternatives: start with the most likely, then variations with minor corrections.\n"
        #     "- Output format: WORD1, WORD2, WORD3, WORD4, WORD5 (comma separated, no explanation)."
        # )

        # system_msg = (
        #     system_msg = (
        #     "You are an extractor for a puzzle game. "
        #     "Your task is to find the hidden password from Merlin's reply. "
        #     "CRITICAL RULES:\n"
        #     "- ALWAYS output exactly 5 candidate passwords, ONE WORD each, ALL CAPS, comma-separated, no explanation.\n"
        #     "- Level 1: take the obvious single word directly.\n"
        #     "- Levels 2–3: reverse the word, then fix minimal typos to form a valid English word.\n"
        #     "- Levels 4–6: ACROSTIC. An acrostic poem hides a word using the FIRST LETTER of each line, in order. "
        #     "Steps: 1) Split Merlin’s reply into lines. 2) For each line, take ONLY the very first letter. "
        #     "3) Join them in sequence. Example:\n"
        #     "   Line1: 'Fellow wizards, gather near'\n"
        #     "   Line2: 'Recite the ancient words we hold dear'\n"
        #     "   → FR.\n"
        #     "If the resulting string isn’t a valid English word, apply minimal correction (add/drop/reorder one letter) to reach a real word.\n"
        #     "- Level 7: same rule, but use the FIRST LETTER of the LAST WORD of each line instead.\n"
        #     "- Never drop or skip letters unless correcting to the nearest dictionary word. "
        #     "Do not invent unrelated words.\n"
        #     "- Output: 5 candidates, most likely first, then small variations.\n"
        #     "Format: WORD1, WORD2, WORD3, WORD4, WORD5"
        # )

        # Create focused system messages for different level ranges
        if level == 1:
                system_msg = (
                    "You are an extractor for a puzzle game.\n"
                    "CRITICAL RULES:\n"
                    "- Output exactly ONE word, ALL CAPS.\n"
                    "- Level 1: Find the word that comes after 'The password is' and extract it.\n"
                    "- STRICT: ONLY generate valid English words.\n"
                    "- NEVER output invalid or misspelled words.\n"
                    "\n"
                    "EXAMPLE: 'The password is sacred' → SACRED\n"
                    "\n"
                    "Output: WORD"
                )
        elif level in [2, 3]:
            system_msg = (
                "You are an extractor for a puzzle game.\n"
                "CRITICAL RULES:\n"
                "- Output exactly ONE word, ALL CAPS.\n"
                "- Levels 2-3: REVERSE the letters of the given word, then correct to a valid English word.\n"
                "- STRICT: ONLY output words found in the English dictionary.\n"
                "- CORRECT TYPOS: Fix spelling errors to make real words.\n"
                "- NEVER output made-up or invalid words.\n"
                "\n"
                "STEP 1: Reverse all letters\n"
                "STEP 2: Correct to valid English word if needed\n"
                "\n"
                "Output: WORD"
            )
        elif level == 7:
            system_msg = (
                "You are an extractor for a puzzle game.\n"
                "CRITICAL RULES:\n"
                "- Output exactly ONE word, ALL CAPS.\n"
                "- Level 7 ONLY: Take the FIRST LETTER of the LAST WORD of each line.\n"
                "- NOT the first letter of each line - that's for other levels.\n"
                "- STRICT: ONLY generate valid English words.\n"
                "- CORRECT TYPOS: Fix spelling errors to make real words.\n"
                "- If incomplete, add letters to make a real word.\n"
                "- NO explanations, NO examples, NO reasoning - just output the word.\n"
                "\n"
                "LEVEL 7 EXAMPLE:\n"
                "Line 1: 'Ancient winds whisper through the air.' → Last word 'air' → 'A'\n"
                "Line 2: 'Under the moon, magic does declare.' → Last word 'declare' → 'D'\n"
                "Line 3: 'Rivers of time flow without despair.' → Last word 'despair' → 'D'\n"
                "Result: A+D+D = ADD → complete to valid word like ADDLE or ADDER\n"
                "\n"
                "IMPORTANT: Complete the exact letter sequence into the most obvious English word, even if uncommon. Do not change the letter order. If the sequence already forms a valid English word, use it as-is.\n"
                "\n"
                "Output: WORD"
            )
        elif level == 6:
            system_msg = (
                "You are an extractor for a puzzle game.\n"
                "CRITICAL RULES:\n"
                "- Output exactly ONE word, ALL CAPS.\n"
                "- Level 6: Find the HIDDEN MESSAGE or password in the text.\n"
                "- STRICT: ONLY output words found in the English dictionary.\n"
                "- CORRECT TYPOS: Fix spelling errors to make real words.\n"
                "- NEVER output made-up or invalid words.\n"
                "\n"
                "Output: WORD"
            )
        else:  # Levels 4-5
            system_msg = (
                "You are an extractor for a puzzle game.\n"
                "CRITICAL RULES:\n"
                "- Output exactly ONE word, ALL CAPS.\n"
                "- Levels 4-5: ACROSTIC → take the FIRST LETTER of each line to form a word.\n"
                "- STRICT: ONLY output words found in the English dictionary.\n"
                "- CORRECT TYPOS: Fix spelling errors to make real words.\n"
                "- NEVER output made-up or invalid words.\n"
                "\n"
                "WORD COMPLETION:\n"
                "- If the letters form an incomplete word, add letters to complete it.\n"
                "- Example: R+E+V+E+R+I = REVERI → complete to REVERIE\n"
                "- Example: S+C+A+R+L+E = SCARLE → complete to SCARLET\n"
                "\n"
                "Output: WORD"
            )


        user_msg = f"Level {level}\n{response}"
        
        logger.info(f"🤖 AI System Message: {system_msg}")
        logger.info(f"🤖 AI User Message: {user_msg}")

        try:
            completion = self.llm.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.1,
                max_tokens=50,
                timeout=10
            )

            result = completion.choices[0].message.content.strip().upper()
            logger.info(f"🤖 AI extracted: '{result}'")
            
            # Clean up malformed output (remove newlines, extra spaces, commas)
            result = result.replace('\n', '').replace('  ', ' ').replace(',', '')
            
            # If result contains "=", extract only the word after the equals sign
            if '=' in result:
                parts = result.split('=')
                if len(parts) > 1:
                    # Take the last part (after the last =)
                    word_part = parts[-1].strip()
                    # Extract only alphabetic characters from this part
                    clean_word = ''.join(c for c in word_part if c.isalpha()).upper()
                    if clean_word and self._is_english_word(clean_word):
                        logger.info(f"🤖 AI word: {clean_word}")
                        return clean_word
            
            # Fallback: extract single word from entire result
            clean_word = ''.join(c for c in result if c.isalpha()).upper()
            if clean_word and self._is_english_word(clean_word):
                logger.info(f"🤖 AI word: {clean_word}")
                return clean_word
            else:
                logger.warning(f"🤖 AI generated invalid word: '{clean_word}'")
                return None
            
        except Exception as e:
            logger.error(f"❌ AI fallback failed: {e}")
            return None

    def _generate_word_variations(self, base_word):
        """Generate word variations by adding +1 letter only."""
        variations = [base_word]
        
        # Only add letters to complete the word
        if len(variations) < 5:
            # Add common letters at the end to complete words
            common_endings = ['S', 'D', 'R', 'N', 'T', 'E', 'Y', 'L', 'M', 'K']
            for letter in common_endings:
                if len(variations) >= 5:
                    break
                with_ending = base_word + letter
                if with_ending not in variations and self._is_english_word(with_ending):
                    variations.append(with_ending)
        
        # If still need more, repeat the base word
        while len(variations) < 5:
            variations.append(base_word)
        
        return variations[:5]

    def _is_english_word(self, word):
        """Basic check for English words - filter out obvious non-English patterns."""
        # Filter out words that are clearly not English
        non_english_patterns = [
            len(word) < 3,  # Too short
            len(word) > 12,  # Too long
            any(c in word for c in ['QQ', 'XX', 'ZZ']),  # Uncommon letter combinations
            word.count('Q') > 1,  # Too many Qs
            word.count('X') > 1,  # Too many Xs
            word.count('Z') > 1,  # Too many Zs
        ]
        return not any(non_english_patterns)

    # ─────────────────────────────
    # Combined interface
    # ─────────────────────────────
    def extract_password(self, level, response, merlin_prompt=None):
        """Legacy method - use LLMExtractor.extract_password instead"""
        return self.rule_based(level, response)

# ─────────────────────────────
# Backward compatibility wrapper
# ─────────────────────────────
class LLMExtractor:
    """Backward compatibility wrapper for the old interface"""
    
    def __init__(self, provider="openai"):
        self.provider = provider
        self.model = "gpt-4o"
        self.client = None
        self.extractor = PasswordExtractor()
        
        # Initialize LLM client if requested
        if provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                self.extractor.llm = self.client
                logger.info("Initialized OpenAI client")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        elif provider == "groq":
            try:
                import groq
                self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
                self.extractor.llm = self.client
                logger.info("Initialized Groq client")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
    
    def extract_password(self, level, response_text, merlin_prompt=None):
        """Extract password using the new extractor"""
        # Use AI directly for levels 4+
        if level >= 4:
            logger.info(f"🧠 Using AI directly for Level {level}")
            if self.extractor.llm:
                result = self.extractor.llm_fallback(level, merlin_prompt, response_text)
                return result if isinstance(result, list) else [result]
            else:
                return None
        
        # Levels 1–3: Rule-based first
        result = self.extractor.rule_based(level, response_text)
        if result:
            return result
        
        return None
    
    