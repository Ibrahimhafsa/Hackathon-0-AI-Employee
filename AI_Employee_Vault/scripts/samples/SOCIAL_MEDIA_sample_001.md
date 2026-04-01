# Social Media Post Tasks - Guide

## How to Use Social Media Tasks (Platinum Tier)

Social media tasks are easy to create! Follow this format to generate post approvals.

### File Naming
- Start with `SOCIAL_` prefix
- Use descriptive name (e.g., `SOCIAL_twitter_launch.md`)
- Save to `Needs_Action/` folder

### Required Fields
Each social media post must include:
- **Platform:** Twitter, X, or LinkedIn
- **Post Content:** The message content

### Optional Fields
- **Hashtags:** Topic tags (comma-separated)
- **Mentions:** @mentions to include (comma-separated)
- **Priority:** Normal, High, or Low

### Example Task

```markdown
# Twitter Post: Feature Announcement

**Platform:** Twitter
**Hashtags:** #NewFeature #AI #Innovation
**Mentions:** @TechBlog @Industry
**Priority:** High

## Post Content

🎉 Introducing our newest AI feature!

Faster processing, better accuracy, and seamless integration.
Available today for all users.

Check it out → [link]

#NewFeature #AI #Innovation
```

## Platform Support

### Twitter / X
- Character limit: 280 characters (recommended to stay under)
- Supports hashtags, mentions, links, emojis
- Good for: Product announcements, news, engagement

### LinkedIn
- Character limit: 3,000 characters
- More professional tone
- Good for: Company news, insights, achievements

### Format Tips
- Keep Twitter posts concise and engaging
- LinkedIn posts can be longer and more detailed
- Always include relevant hashtags
- Use emojis appropriately for your platform
- Include call-to-action if applicable

## How It Works

1. **Create**: Place your post task file in `Needs_Action/`
2. **Detect**: Social Media Generator monitors and finds your file
3. **Validate**: Post content and platform are verified
4. **Generate**: An approval file is created in `Pending_Approval/`
5. **Review**: Open and review the post in the approval file
6. **Approve**: Move file to `Approved/` folder
7. **Execute**: Action Executor logs the post (DRY RUN - no actual post)
8. **Done**: File moves to `Done/` folder

## DRY RUN Mode

Platinum Tier runs in **DRY RUN mode**, meaning:
- ✅ Posts are generated and logged
- ✅ Full post content is recorded
- ✅ Approval workflow is tested
- ❌ No actual posts are created
- ❌ No social media accounts are contacted

Perfect for testing and learning!

## Logs

All social media processing is logged to:
- `Logs/social_media_generator_*.log` - Post generation logs
- `Logs/action_executor_*.log` - Posting/execution logs

View logs to see:
- Detected social media tasks
- Generated approval requests
- Simulated post creation
- Full post content that was "posted"

## Examples

### Short Twitter Post
```markdown
# Twitter: Flash Sale

**Platform:** Twitter
**Hashtags:** #Sale #LimitedTime
**Priority:** High

## Post Content

⏰ Flash Sale: 50% off for 24 hours only!

Get it now → [link]

#Sale #LimitedTime
```

### Detailed LinkedIn Post
```markdown
# LinkedIn: Industry Insights

**Platform:** LinkedIn
**Hashtags:** #Innovation #FutureOfWork #AI
**Priority:** Normal

## Post Content

The future of work is here. Here's what we learned:

1. Remote teams need better collaboration tools
2. AI can automate routine tasks
3. Human creativity remains irreplaceable

Our latest report covers these insights in detail.

[Download report]

#Innovation #FutureOfWork #AI
```

### Campaign Post
```markdown
# Twitter: Campaign Launch

**Platform:** Twitter
**Hashtags:** #NewCampaign #JoinUs #MakesADifference
**Mentions:** @Partners @Community
**Priority:** High

## Post Content

We're launching a new initiative to help thousands of people.

Join us! Every action counts.

Learn more & get involved → [link]

#NewCampaign #JoinUs #MakesADifference
```

## Best Practices

1. **Platform-specific**: Tailor tone and length to platform
2. **Hashtags**: Use relevant, trending hashtags (3-5 recommended)
3. **Engagement**: Include call-to-action when appropriate
4. **Links**: Always include links to resources mentioned
5. **Timing**: Consider best times to post (not in task)
6. **Review**: Check spelling and links before approving
7. **Compliance**: Follow platform guidelines and brand voice

## Troubleshooting

### "No approvals created"
1. Check filename: must start with `SOCIAL_`
2. Check extension: must be `.md`
3. Check social media generator is running
4. Wait a few seconds (polling interval)

### "Invalid platform"
- Only Twitter, X, and LinkedIn supported
- Check platform field spelling (case-insensitive)

### "Missing content"
- Ensure `## Post Content` section exists
- Content must be at least 10 characters

---
Created for AI Employee Vault - Platinum Tier Social Media Integration
