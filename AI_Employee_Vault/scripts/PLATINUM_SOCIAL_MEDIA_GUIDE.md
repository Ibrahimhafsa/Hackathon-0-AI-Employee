# Platinum Tier Social Media Integration - Quick Start

## Overview

Platinum Tier adds **Social Media Posting** to your AI Employee system. Create posts for Twitter/X and LinkedIn, get them approved, and watch them get logged (DRY RUN mode - no actual posting).

## Quick Start (5 minutes)

### 1. Start the Social Media Generator
```bash
python3 scripts/social_media_generator.py
```

You'll see:
```
SOCIAL MEDIA GENERATOR STARTED (PLATINUM TIER - DRY RUN MODE)
Watching directory: .../Needs_Action
✅ Generator is running. Waiting for social media tasks...
```

### 2. Create a Social Media Task
Create file: `Needs_Action/SOCIAL_hello_001.md`

```markdown
# Twitter Post: Hello World

**Platform:** Twitter
**Hashtags:** #AI #AutomatedPosting
**Priority:** Normal

## Post Content

Hello from the AI Employee system! 👋

Testing social media automation with DRY RUN mode.

#AI #AutomatedPosting
```

### 3. Watch It Get Detected
In your social media generator terminal:
```
📱 Social media task detected: SOCIAL_hello_001.md
✅ Post approval created: SOCIAL_APPROVAL_SOCIAL_hello_001.json
→ Platform: twitter
→ Content preview: Hello from the AI Employee system!...
→ Mode: DRY RUN (will not actually post)
```

### 4. Review the Approval
```bash
cat Pending_Approval/SOCIAL_APPROVAL_SOCIAL_hello_001.json
```

You'll see all post details in JSON format.

### 5. Approve the Post
```bash
# Move to Approved folder to approve
mv Pending_Approval/SOCIAL_APPROVAL_SOCIAL_hello_001.json Approved/
```

### 6. Execute (Simulate Post)
```bash
python3 scripts/action_executor.py --once
```

Output:
```
🚀 Executing action: post_social_media
   [DRY RUN MODE] No actual action will be performed
   Recipient: N/A
   Subject: No subject
   📱 [DRY RUN] Would post to social media
      Platform: Twitter
      Priority: Normal
      Full content:
         Hello from the AI Employee system! 👋
         
         Testing social media automation with DRY RUN mode.
      Hashtags: #AI #AutomatedPosting
   ✓ Action completed successfully
```

### 7. Check the Log
```bash
tail -30 Logs/action_executor_*.log
```

See the full post that was "posted"!

---

## Post Format

### Required Fields
```markdown
**Platform:** Twitter or LinkedIn
## Post Content
Your message here...
```

### Optional Fields
```markdown
**Hashtags:** #tag1 #tag2 #tag3
**Mentions:** @user1 @user2
**Priority:** High | Normal | Low
```

### Complete Example
```markdown
# Twitter: Product Update

**Platform:** Twitter
**Hashtags:** #NewFeature #ProductUpdate
**Mentions:** @Customers @Team
**Priority:** High

## Post Content

🎉 New feature released!

Check out our latest update and let us know what you think.

Available now for all users.

[Learn more](link)
```

---

## Platform Support

### Twitter / X
- Max 280 characters recommended
- Perfect for news and quick updates
- Good engagement with hashtags

### LinkedIn
- Up to 3,000 characters
- Professional audience
- Great for company milestones

---

## File Naming

**Important:** Posts MUST start with `SOCIAL_`

✅ Good:
- `SOCIAL_twitter_news.md`
- `SOCIAL_linkedin_milestone.md`
- `SOCIAL_x_announcement.md`

❌ Bad:
- `social_twitter_news.md` (lowercase)
- `TWITTER_news.md` (no SOCIAL_ prefix)
- `SOCIAL_news.txt` (wrong extension)

---

## Workflow Steps

```
1. Create file: Needs_Action/SOCIAL_*.md
   ↓
2. Social Media Generator detects file
   ↓
3. Creates: Pending_Approval/SOCIAL_APPROVAL_*.json
   ↓
4. YOU review and approve
   ↓
5. Move to: Approved/
   ↓
6. Action Executor simulates post
   ↓
7. Logs to: Logs/action_executor_*.log
   ↓
8. Moves to: Done/
```

---

## Running Everything Together

### Terminal 1: Plan Generator (Silver Tier)
```bash
python3 scripts/plan_generator.py
```

### Terminal 2: Approval Manager (Silver Tier)
```bash
python3 scripts/approval_manager.py
```

### Terminal 3: Email Generator (Gold Tier)
```bash
python3 scripts/email_generator.py
```

### Terminal 4: Social Media Generator (Platinum Tier) ← NEW
```bash
python3 scripts/social_media_generator.py
```

### Terminal 5: Action Executor (All Tiers)
```bash
python3 scripts/action_executor.py
```

Now you have complete automation!

---

## DRY RUN Mode

**DRY RUN = Safe Testing Mode**

What happens:
- ✅ Post tasks are created and tracked
- ✅ Approval requests are generated
- ✅ Full post content is logged
- ❌ NO actual posts are created
- ❌ No social media accounts contacted

Why use it:
- Test posting workflow safely
- Learn system without side effects
- Development and staging use
- Build confidence before real posts

---

## Checking Results

### See Generated Approvals
```bash
ls Pending_Approval/SOCIAL_APPROVAL_*.json
```

### View Post Approval Details
```bash
cat Pending_Approval/SOCIAL_APPROVAL_SOCIAL_hello_001.json
```

### Check Execution Logs
```bash
# Latest action executor log
tail -50 Logs/action_executor_*.log

# Search for social posts
grep "post_social_media" Logs/action_executor_*.log

# Search for specific platform
grep "Platform: twitter" Logs/action_executor_*.log
```

### View Completed Tasks
```bash
ls Done/SOCIAL_APPROVAL_*.json
```

---

## Troubleshooting

### "No approvals created"
1. Check filename: must start with `SOCIAL_`
2. Check extension: must be `.md`
3. Check social media generator is running
4. Wait a few seconds (polling interval)
5. Check log: `tail Logs/social_media_generator_*.log`

### "Invalid platform"
- Valid platforms: twitter, x, linkedin
- Check spelling in `**Platform:**` field

### "Missing post content"
- Ensure `## Post Content` section exists
- Content must be at least 10 characters

### "Post not executing"
- Check action executor is running
- Check file is in `Approved/` folder (not `Pending_Approval/`)
- Check JSON format is valid
- Run with `--once` flag manually

---

## Example Tasks

### 1. Simple Twitter Update
```markdown
# Twitter: Daily Tip

**Platform:** Twitter
**Hashtags:** #DailyTip #AI #Productivity
**Priority:** Normal

## Post Content

💡 Daily Tip: Automation saves time.

Let AI handle routine tasks while you focus on what matters.

#DailyTip #AI #Productivity
```

### 2. LinkedIn Announcement
```markdown
# LinkedIn: New Office

**Platform:** LinkedIn
**Hashtags:** #Expansion #Growth #Hiring
**Priority:** High

## Post Content

Exciting news! We've opened a new office in [City].

This expansion allows us to serve more customers and grow our incredible team.

Now hiring! Check our careers page for open positions.

#Expansion #Growth #Hiring
```

### 3. Campaign Post
```markdown
# Twitter: Event Announcement

**Platform:** Twitter
**Hashtags:** #WebinarLive #AI #Learning
**Mentions:** @Speakers @Community
**Priority:** High

## Post Content

🎬 Join us tomorrow for a live webinar!

Topic: The Future of AI in Business
Time: 2 PM EST
Register: [link]

#WebinarLive #AI #Learning
```

---

## Tips & Best Practices

### Tip 1: Test First
Create test posts to yourself before posting company announcements.

### Tip 2: Review Content
Always review post content in the approval file before approving.

### Tip 3: Platform Tone
- Twitter: Conversational, concise, engaging
- LinkedIn: Professional, thoughtful, detailed

### Tip 4: Hashtags
Use 3-5 relevant hashtags per post. Check if they're trending.

### Tip 5: Links
Always test links before posting. Broken links hurt engagement.

### Tip 6: Timing
Note: This system doesn't schedule posts. All posts "post" immediately when executed.

---

## Next Steps

1. ✅ Start social media generator
2. ✅ Create SOCIAL_*.md task
3. ✅ Review approval JSON
4. ✅ Move to Approved/
5. ✅ Run executor
6. ✅ Check logs

Then explore:
- Multiple posts at once
- Different platforms
- Various hashtags and mentions
- Integration with other tiers

---

## Need Help?

Check these files:
- `scripts/samples/SOCIAL_MEDIA_sample_001.md` - Detailed examples
- `Logs/social_media_generator_*.log` - Generation debug info
- `Logs/action_executor_*.log` - Execution details

---

**Platinum Tier Social Media Integration - Ready to use!**

Start creating posts and automating your social media workflow. Happy posting! 📱

---

*Created: April 1, 2026*  
*Status: ✅ Complete & Ready*  
*Mode: DRY RUN*
