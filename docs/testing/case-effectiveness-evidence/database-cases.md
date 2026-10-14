# PostgreSQL cases

Each row is an individually executed case. PASS means the current implementation passed its assertions; fault IDs name experiments in which that same case failed.

| Case | Requirement / location | Baseline | Detected faults |
|---|---|---|---|
| F015-plain | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-emoji | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-family | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-skin | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-flag | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-keycap | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-accent | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-cjk | Database uses the pinned grapheme-weighting rule | PASS | SQL-M001 |
| F015-empty | Database uses the pinned grapheme-weighting rule | PASS | SQL-M002 |
| limit-title-174 | Weighted text limit also applies to updates | PASS | SQL-M003 |
| limit-title-175 | Weighted text limit also applies to updates | PASS | SQL-M003 |
| limit-title-176 | Weighted text limit also applies to updates | PASS | SQL-M004 |
| F020 | Combining graphemes fit at the limit | PASS | SQL-M003 |
| draft-title-overflow | Drafts cannot bypass text limits | PASS | SQL-M004 |
| emoji-title-overflow | Emoji weigh four in direct SQL | PASS | SQL-M004 |
| limit-body-6999 | Weighted text limit also applies to updates | PASS | SQL-M003 |
| limit-body-7000 | Weighted text limit also applies to updates | PASS | SQL-M003 |
| limit-body-7001 | Weighted text limit also applies to updates | PASS | SQL-M005 |
| F021 | Combining graphemes fit at the limit | PASS | SQL-M003 |
| draft-body-overflow | Drafts cannot bypass text limits | PASS | SQL-M005 |
| emoji-body-overflow | Emoji weigh four in direct SQL | PASS | SQL-M005 |
| F031 | Blank titles normalize to NULL and preserve body | PASS | SQL-M006 |
| F033 | Nonblank title whitespace is preserved | PASS | SQL-M007 |
| F034 | Body whitespace is preserved | PASS | SQL-M008 |
| F036 | Fully blank saved rows reject | PASS | SQL-M006, SQL-M009 |
| F037 | Fully blank drafts are permitted without countdown | PASS | SQL-M010 |
| F038 | Title-only notes persist with a one-day deadline | PASS | SQL-M011 |
| F039 | Body-only notes persist | PASS | SQL-M013 |
| F040 | Spaces and blank lines do not make saved content | PASS | SQL-M006, SQL-M009 |
| F049-F050 | Multiple users can omit email | PASS | SQL-M014 |
| F051 | Case variants of an email are duplicates | PASS | SQL-M015 |
| email-insert-duplicate | Email uniqueness also rejects a new user | PASS | SQL-M015 |
| email-blank | Direct SQL email must be nonblank and unpadded | PASS | SQL-M017, SQL-M016 |
| email-spaces | Direct SQL email must be nonblank and unpadded | PASS | SQL-M017, SQL-M016 |
| email-leading | Direct SQL email must be nonblank and unpadded | PASS | SQL-M017, SQL-M016 |
| email-trailing | Direct SQL email must be nonblank and unpadded | PASS | SQL-M017, SQL-M016 |
| username-null | Username is required lowercase ASCII with a 20-character cap | PASS | SQL-M018 |
| username-upper | Username is required lowercase ASCII with a 20-character cap | PASS | SQL-M019 |
| username-empty | Username is required lowercase ASCII with a 20-character cap | PASS | SQL-M019 |
| username-twenty-one | Username is required lowercase ASCII with a 20-character cap | PASS | SQL-M019 |
| username-punctuation | Username is required lowercase ASCII with a 20-character cap | PASS | SQL-M019 |
| username-twenty | Twenty-character username accepts and canonical lookup agrees | PASS | SQL-M020 |
| username-duplicate | Duplicate username is rejected | PASS | SQL-M021 |
| F059 | Canonical username cannot be supplied independently | PASS | SQL-M022 |
| F061-user | User default ID is a UUIDv4 | PASS | SQL-M023 |
| F061-note | Note default ID is independent UUIDv4 | PASS | SQL-M024 |
| uuid-users-version | Explicit IDs must have UUIDv4 version and variant | PASS | SQL-M025 |
| uuid-users-variant | Explicit IDs must have UUIDv4 version and variant | PASS | SQL-M025 |
| uuid-notes-version | Explicit IDs must have UUIDv4 version and variant | PASS | SQL-M026 |
| uuid-notes-variant | Explicit IDs must have UUIDv4 version and variant | PASS | SQL-M026 |
| F064 | Duplicate note ID rejects | PASS | SQL-M027 |
| F065 | Owner is required | PASS | SQL-M028 |
| F066 | Owner must exist | PASS | SQL-M029 |
| F067 | Deleting one user cascades only their notes | PASS | SQL-M030 |
| F068 | Immutable identity/creation fields cannot be changed | PASS | SQL-M031 |
| F069 | Immutable identity/creation fields cannot be changed | PASS | SQL-M031 |
| F070 | Immutable identity/creation fields cannot be changed | PASS | SQL-M031 |
| F078 | Immutable identity/creation fields cannot be changed | PASS | SQL-M031 |
| F079 | Immutable identity/creation fields cannot be changed | PASS | SQL-M031 |
| F080 | Immutable identity/creation fields cannot be changed | PASS | SQL-M031 |
| F071 | App role sees only its actor's rows | PASS | SQL-M032 |
| F072 | App cannot edit another actor's note | PASS | SQL-M032 |
| F073 | App cannot insert for another actor | PASS | SQL-M032 |
| F074 | Missing actor sees no protected rows | PASS | SQL-M032 |
| F075-role | App cannot escalate to object owner | PASS | SQL-M033 |
| app-column-id | Column grants forbid app changes to protected fields | PASS | SQL-M034 |
| app-column-user_id | Column grants forbid app changes to protected fields | PASS | SQL-M035 |
| app-column-created_at | Column grants forbid app changes to protected fields | PASS | SQL-M036 |
| app-column-updated_at | Column grants forbid app changes to protected fields | PASS | SQL-M037 |
| app-column-blank_body_expires_at | Column grants forbid app changes to protected fields | PASS | SQL-M038 |
| app-own-edit | App can edit its own content | PASS | SQL-M039 |
| app-saved-delete | App cannot permanently delete a saved note | PASS | SQL-M040 |
| app-blank-draft-delete | App can delete its own blank draft | PASS | SQL-M041 |
| F076 | Device cannot forge server-created time | PASS | SQL-M042 |
| F077 | Initial server times are equal | PASS | SQL-M042 |
| F081 | Content edits advance server edit time | PASS | SQL-M044 |
| F082 | No-op save keeps Last Edited | PASS | SQL-M043 |
| F083 | Hiding a note keeps Last Edited | PASS | SQL-M043 |
| F084 | Restoring a note keeps Last Edited | PASS | SQL-M043 |
| F085 | Manual server edit time is overridden for no-op | PASS | SQL-M043 |
| F086 | Initial device edit time equals device creation | PASS | SQL-M045 |
| F087 | Device time cannot control expiry | PASS | SQL-M011 |
| F088 | Device time cannot control retention | PASS | SQL-M046 |
| F089 | Different timezone offsets preserve an instant | PASS | SQL-M047 |
| F090 | Device-only metadata update does not fake a text edit | PASS | SQL-M043 |
| F092 | Title-only draft has no countdown | PASS | SQL-M010 |
| F093 | Adding real body clears countdown | PASS | SQL-M048 |
| F094 | Returning to blank starts a new countdown | PASS | SQL-M011 |
| F095 | A saved blank-body deadline cannot be extended or removed | PASS | SQL-M012 |
| F096 | A saved blank-body deadline cannot be extended or removed | PASS | SQL-M012 |
| F097 | A saved blank-body deadline cannot be extended or removed | PASS | SQL-M012 |
| F098 | A saved blank-body deadline cannot be extended or removed | PASS | SQL-M012 |
| F099 | Saved notes cannot become drafts | PASS | SQL-M049 |
| F100 | Worker cannot expire a future title-only note | PASS | SQL-M050 |
| F102 | Overdue title-only notes enter trash instead of disappearing | PASS | SQL-M051 |
| F103 | Worker leaves filled notes alone | PASS | SQL-M050 |
| F104 | Repeated expiry keeps first trash time | PASS | SQL-M050 |
| F106 | New notes cannot be inserted into trash | PASS | SQL-M046 |
| F107 | Caller cannot forge deletion time | PASS | SQL-M046 |
| F108 | Repeated hiding preserves first deletion time | PASS | SQL-M046 |
| F109 | Active view excludes trash | PASS | SQL-M052 |
| F110 | Fresh trash can be restored | PASS | SQL-M053 |
| F112 | Restore after retention is rejected | PASS | SQL-M046 |
| F113 | Fresh trash survives purge | PASS | SQL-M054 |
| F115 | Active rows survive purge | PASS | SQL-M054 |
| purge-overdue | Overdue trash is removed | PASS | SQL-M055 |
| F116 | Trashed body cannot be edited | PASS | SQL-M046 |
| F117 | Trashed draft cannot be published | PASS | SQL-M046 |
| F118 | Restored title-only note gets a new countdown | PASS | SQL-M011 |
| sql-batch-cleanup_expired_blank_notes-NULL | SQL cleanup refuses invalid batch sizes | PASS | SQL-M051 |
| sql-batch-cleanup_expired_blank_notes-0 | SQL cleanup refuses invalid batch sizes | PASS | SQL-M051 |
| sql-batch-cleanup_expired_blank_notes-1001 | SQL cleanup refuses invalid batch sizes | PASS | SQL-M051 |
| sql-batch-purge_deleted_notes-NULL | SQL cleanup refuses invalid batch sizes | PASS | SQL-M055 |
| sql-batch-purge_deleted_notes-0 | SQL cleanup refuses invalid batch sizes | PASS | SQL-M055 |
| sql-batch-purge_deleted_notes-1001 | SQL cleanup refuses invalid batch sizes | PASS | SQL-M055 |
| maintenance-fresh-delete | Maintenance cannot delete recent trash | PASS | SQL-M056 |
| maintenance-active-read | Maintenance cannot read non-due active content | PASS | SQL-M057 |
| maintenance-overdue-purge | Maintenance can purge only due trash | PASS | SQL-M055 |
| maintenance-expiry | Maintenance can expire due rows | PASS | SQL-M051 |
| F045-nbsp | Python and SQL agree that nonbreaking-space-only body is blank | PASS | SQL-M006, SQL-M009 |
| F053-nbsp | Direct SQL rejects nonbreaking-space padding on email | PASS | SQL-M017, SQL-M016 |
| F091 | New title-only note starts exactly one day after server creation | PASS | SQL-M011 |
| F101 | Expiry includes the exact server-statement deadline | PASS | SQL-M051 |
| F114 | Purge includes the exact retention boundary | PASS | SQL-M055 |
| app-own-insert | App can insert for its own actor | PASS | SQL-M039 |
| app-crossuser-delete | App cannot delete another user's account or note | PASS | SQL-M032 |
| app-unset-actor | Unset actor fails closed | PASS | SQL-M032 |
| app-active-view | Active view preserves the actor boundary | PASS | SQL-M032 |
| required-body | Required note data cannot be NULL | PASS | SQL-M058 |
| required-device_created_at | Required note data cannot be NULL | PASS | SQL-M059 |
| required-is_draft | Required note data cannot be NULL | PASS | SQL-M060 |
| permission-groups | All permission groups lack administrative or login powers | PASS | SQL-M061 |
| rls-forced | Both tables have forced row policies | PASS | SQL-M062 |
| app-no-cleanup-grant | App cannot execute maintenance functions | PASS | SQL-M063 |
| app-no-schema-create | App cannot create public schema objects | PASS | SQL-M064 |
| index-created | Timeline index has the intended owner/order keys | PASS | SQL-M065 |
| index-edited | Timeline index has the intended owner/order keys | PASS | SQL-M066 |
| index-device | Timeline index has the intended owner/order keys | PASS | SQL-M067 |
| index-draft | Timeline index has the intended owner/order keys | PASS | SQL-M068 |
| app-delete-account-cascade | Deleting one's own account removes saved notes too | PASS | SQL-M030 |
| sql-valid-batch-cleanup_expired_blank_notes-1 | SQL accepts both valid batch boundaries | PASS | SQL-M050 |
| sql-valid-batch-cleanup_expired_blank_notes-1000 | SQL accepts both valid batch boundaries | PASS | SQL-M050 |
| sql-valid-batch-purge_deleted_notes-1 | SQL accepts both valid batch boundaries | PASS | SQL-M054 |
| sql-valid-batch-purge_deleted_notes-1000 | SQL accepts both valid batch boundaries | PASS | SQL-M054 |
| expiry-batch-one | Expiry processes the oldest due row and respects batch one | PASS | SQL-M051 |
| purge-batch-one | Purge processes the oldest trash and respects batch one | PASS | SQL-M055 |
| note-body-default | Omitted body defaults to empty text and gets a saved countdown | PASS | SQL-M011 |
| user-id-duplicate | A duplicate user ID rejects even with a different username | PASS | SQL-M069 |
| user-clock-forged | User server clocks also override device-forged insert values | PASS | SQL-M042 |
| unicode-blank-title | Nonbreaking-space-only titles normalize to NULL | PASS | SQL-M006 |
| unicode-blank-countdown | Nonbreaking-space-only body starts a title-only countdown | PASS | SQL-M006, SQL-M011 |
| unicode-email-padding-leading | Each Unicode-padding edge is rejected independently | PASS | SQL-M016, SQL-M017 |
| unicode-email-padding-trailing | Each Unicode-padding edge is rejected independently | PASS | SQL-M016, SQL-M017 |
| unicode-blank-draft-delete | App can delete a draft that Python considers fully blank | PASS | SQL-M006, SQL-M041 |
| blank-body-U+0009 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+000A | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+000B | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+000C | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+000D | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+001C | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+001D | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+001E | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+001F | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+0020 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+0085 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+1680 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2000 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2001 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2002 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2003 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2004 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2005 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2006 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2007 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2008 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2009 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+200A | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2028 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+2029 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+202F | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+205F | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| blank-body-U+3000 | Unicode whitespace alone cannot be saved as note content | PASS | SQL-M006, SQL-M009 |
| parity-U+0009-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+0009-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+0009-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0009-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0009-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0009-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+0009-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+000A-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+000A-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+000A-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000A-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000A-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000A-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+000A-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+000B-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+000B-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+000B-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000B-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000B-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000B-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+000B-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+000C-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+000C-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+000C-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000C-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000C-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000C-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+000C-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+000D-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+000D-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+000D-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000D-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000D-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+000D-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+000D-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+001C-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+001C-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+001C-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001C-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001C-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001C-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+001C-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+001D-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+001D-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+001D-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001D-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001D-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001D-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+001D-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+001E-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+001E-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+001E-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001E-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001E-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001E-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+001E-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+001F-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+001F-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+001F-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001F-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001F-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+001F-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+001F-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+0020-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+0020-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+0020-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0020-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0020-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0020-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+0020-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+0085-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+0085-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+0085-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0085-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0085-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+0085-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+0085-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+00A0-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+00A0-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+00A0-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+00A0-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+00A0-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+00A0-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+00A0-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+1680-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+1680-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+1680-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+1680-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+1680-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+1680-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+1680-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2000-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2000-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2000-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2000-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2000-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2000-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2000-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2001-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2001-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2001-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2001-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2001-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2001-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2001-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2002-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2002-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2002-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2002-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2002-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2002-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2002-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2003-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2003-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2003-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2003-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2003-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2003-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2003-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2004-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2004-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2004-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2004-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2004-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2004-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2004-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2005-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2005-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2005-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2005-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2005-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2005-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2005-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2006-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2006-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2006-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2006-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2006-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2006-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2006-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2007-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2007-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2007-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2007-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2007-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2007-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2007-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2008-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2008-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2008-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2008-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2008-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2008-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2008-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2009-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2009-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2009-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2009-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2009-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2009-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2009-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+200A-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+200A-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+200A-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+200A-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+200A-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+200A-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+200A-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2028-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2028-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2028-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2028-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2028-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2028-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2028-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+2029-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+2029-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+2029-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2029-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2029-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+2029-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+2029-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+202F-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+202F-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+202F-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+202F-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+202F-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+202F-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+202F-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+205F-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+205F-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+205F-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+205F-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+205F-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+205F-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+205F-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-U+3000-title | All blank titles normalize to NULL | PASS | SQL-M006 |
| parity-U+3000-countdown | All blank saved bodies start the 24-hour countdown | PASS | SQL-M006, SQL-M011 |
| parity-U+3000-email-leading | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+3000-email-trailing | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+3000-email-blank | SQL rejects every blank/padded stored email | PASS | SQL-M016, SQL-M017 |
| parity-U+3000-draft-delete | Owner can delete every whitespace-only draft | PASS | SQL-M006, SQL-M041 |
| parity-U+3000-maintenance | Limited worker sees and expires every due blank body | PASS | SQL-M006, SQL-M051 |
| parity-nonwhitespace-U+200B | Invisible nonwhitespace remains real SQL content | PASS | SQL-M070 |
| parity-nonwhitespace-U+FEFF | Invisible nonwhitespace remains real SQL content | PASS | SQL-M070 |
| parity-nonwhitespace-U+2060 | Invisible nonwhitespace remains real SQL content | PASS | SQL-M070 |
| test_failed_second_write_rolls_back_first_write_after_reconnect | Failed second write rolls back first after reconnect | PASS | SQL-M071 |

[Fault catalogue](fault-catalogue.md) · [Audit report](../case-effectiveness-audit.md)
