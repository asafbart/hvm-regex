/**
 * @file hvm_regex.h
 * @brief C interface to the HVM regex engine
 */

#ifndef HVM_REGEX_H
#define HVM_REGEX_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Opaque handle to a compiled regex pattern
 */
typedef struct hvm_regex_pattern* hvm_regex_t;

/**
 * Match result structure
 */
typedef struct {
    int position;     /**< Starting position of the match */
    int length;       /**< Length of the matched text */
    int success;      /**< 1 if match succeeded, 0 otherwise */
} hvm_regex_match_t;

/**
 * Compile a regex pattern
 * 
 * @param pattern The regex pattern string
 * @return A handle to the compiled pattern, or NULL if compilation failed
 */
hvm_regex_t hvm_regex_compile(const char* pattern);

/**
 * Free a compiled regex pattern
 * 
 * @param regex The compiled pattern to free
 */
void hvm_regex_free(hvm_regex_t regex);

/**
 * Match a compiled pattern against text
 * 
 * @param regex The compiled pattern
 * @param text The text to match against
 * @param length Length of the text
 * @param start_pos Starting position in the text
 * @param match Output match result
 * @return 1 if match succeeded, 0 otherwise
 */
int hvm_regex_match(hvm_regex_t regex, 
                    const char* text, 
                    size_t length, 
                    size_t start_pos, 
                    hvm_regex_match_t* match);

/**
 * Match a pattern string against text (convenience function)
 * 
 * @param pattern The regex pattern string
 * @param text The text to match against
 * @param length Length of the text
 * @param start_pos Starting position in the text
 * @param match Output match result
 * @return 1 if match succeeded, 0 otherwise
 */
int hvm_regex_match_string(const char* pattern, 
                          const char* text, 
                          size_t length, 
                          size_t start_pos, 
                          hvm_regex_match_t* match);

/**
 * Find all matches of a pattern in text
 * 
 * @param regex The compiled pattern
 * @param text The text to search
 * @param length Length of the text
 * @param matches Array to store matches
 * @param max_matches Maximum number of matches to store
 * @return Number of matches found
 */
int hvm_regex_find_all(hvm_regex_t regex, 
                       const char* text, 
                       size_t length, 
                       hvm_regex_match_t* matches, 
                       size_t max_matches);

/**
 * Get the version of the HVM regex engine
 * 
 * @return Version string
 */
const char* hvm_regex_version(void);

#ifdef __cplusplus
}
#endif

#endif /* HVM_REGEX_H */